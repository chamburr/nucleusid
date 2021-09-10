from typing import Optional

from flask import Blueprint
from flask_login import current_user, login_required
from webargs import fields, validate

from server.models.folder import Folder
from server.models.person import Person
from server.models.share import Share
from server.routes import Response, parse_body, respond_default, respond_error
from server.utils import mail
from server.utils.encryption import SecretCipher

bp = Blueprint("folders", __name__)


def get_folder(item: int) -> Optional[Folder]:
    folder = Folder.find(item)
    if folder is None:
        return None

    if folder.person == current_user.id:
        return folder

    if folder.sharing is False:
        return None

    share = Share.find(folder.id, current_user.id)
    if share is None or share.confirmed is False:
        return None

    return folder


def get_folder_share(
    item: int, item2: int
) -> tuple[Optional[Folder], Optional[Share]]:
    folder = Folder.find(item)
    if folder is None:
        return None, None

    if folder.sharing is False:
        return folder, None

    share = Share.find(folder.id, item2)
    if share is None or share.confirmed is False:
        return folder, None

    return folder, share


@bp.get("/folders")
@login_required
def get_folders() -> Response:
    folders = []

    for folder in Folder.find_by_person(current_user.id):
        folders.append(folder.to_dict())

    return {"folders": folders}


@bp.post("/folders")
@login_required
@parse_body(
    name=fields.Str(required=True, validate=validate.Length(2, 32)),
)
def post_folders(body: dict) -> Response:
    if len(Folder.find_by_person(current_user.id)) >= 10:
        respond_error(400, "Maximum number of folders is reached.")

    folder = Folder.create(person=current_user.id, name=body["name"])

    return folder.to_dict()


@bp.get("/folders/<int:item>")
@login_required
def get_folders_item(item: int) -> Response:
    folder = get_folder(item)
    if folder is None:
        return respond_error(404)

    return folder.to_dict()


@bp.patch("/folders/<int:item>")
@login_required
@parse_body(
    name=fields.Str(validate=validate.Length(2, 32)),
    sharing=fields.Bool(),
)
def patch_folders_item(body: dict, item: int) -> Response:
    folder = get_folder(item)
    if folder is None:
        return respond_error(404)

    if folder.person != current_user.id:
        return respond_error(403)

    if folder.built_in is True:
        return respond_error(400, "Default folder cannot be edited.")

    if body.get("name") is not None:
        folder.update(name=body["name"])

    if body.get("sharing") is not None:
        folder.update_sharing(current_user.secret_cipher(), body["sharing"])

    return respond_default()


@bp.delete("/folders/<int:item>")
@login_required
def delete_folders_item(item: int) -> Response:
    folder = get_folder(item)
    if folder is None:
        return respond_error(404)

    if folder.person != current_user.id:
        return respond_error(403)

    if folder.built_in is True:
        return respond_error(400, "Default folder cannot be deleted.")

    if folder.sharing is True:
        return respond_error(400, "Folder cannot be deleted when shared.")

    folder.delete()

    return respond_default()


@bp.get("/folders/<int:item>/shares")
@login_required
def get_folders_item_shares(item: int) -> Response:
    folder = get_folder(item)
    if folder is None:
        return respond_error(404)

    shares = []

    for share in Share.find_by_folder(folder.id):
        share = share.to_dict()
        del share["folder"]
        del share["secret"]

        shares.append(share)

    return {"shares": shares}


@bp.post("/folders/<int:item>/shares")
@login_required
@parse_body(
    email=fields.Email(required=True),
    view_only=fields.Bool(required=True),
)
def post_folders_item_shares(body: dict, item: int) -> Response:
    folder = get_folder(item)
    if folder is None:
        return respond_error(404)

    if folder.sharing is False:
        return respond_error(400, "Folder sharing is disabled.")

    if folder.person != current_user.id:
        return respond_error(403)

    person = Person.find_by_email(body["email"])
    if person is None:
        return respond_error(400, "The user cannot be found.")

    shares = Share.find_by_folder(folder.id)

    if next((x for x in shares if x.person == person.id), None) is not None:
        return respond_error(400, "Folder is already shared with the user.")

    if len(shares) >= 5:
        return respond_error(400, "Maximum number of shares is reached.")

    share = next(x for x in shares if x.person == current_user.id)
    cipher = SecretCipher.from_public_key(person.public_key)
    secret = cipher.re_encrypt(current_user.secret_cipher(), share.secret)

    new_share = Share.create(
        folder=folder.id,
        person=person.id,
        view_only=body["view_only"],
        secret=secret,
    )

    mail.send_share(current_user.person(), person, new_share)

    return respond_default()


@bp.get("/folders/<int:item>/shares/<int:item2>")
@login_required
def get_folders_item_shares_item2(item: int, item2: int) -> Response:
    folder, share = get_folder_share(item, item2)
    if folder is None or share is None:
        return respond_error(404)

    share = share.to_dict()
    del share["folder"]
    del share["secret"]

    return share


@bp.patch("/folders/<int:item>/shares/<int:item2>")
@login_required
@parse_body(
    view_only=fields.Bool(),
)
def patch_folders_item_shares_item2(
    body: dict, item: int, item2: int
) -> Response:
    folder, share = get_folder_share(item, item2)
    if folder is None or share is None:
        return respond_error(404)

    if folder.person != current_user.id:
        return respond_error(403)

    if folder.person == share.person:
        return respond_error(400, "Owner settings cannot be edited.")

    share.update(view_only=body.get("view_only"))

    return respond_default()


@bp.delete("/folders/<int:item>/shares/<int:item2>")
@login_required
def delete_folders_item_shares_item2(item: int, item2: int) -> Response:
    folder, share = get_folder_share(item, item2)
    if folder is None or share is None:
        return respond_error(404)

    if folder.person != current_user.id:
        return respond_error(403)

    if folder.person == share.person:
        return respond_error(400, "Owner cannot be removed.")

    share.delete()

    return respond_default()
