from typing import Optional

from flask import Blueprint
from flask_login import current_user, login_required
from webargs import fields, validate

from server.models.account import Account
from server.models.folder import Folder
from server.models.share import Share
from server.routes import Response, parse_body, respond_default, respond_error

bp = Blueprint("accounts", __name__)


def get_account(item: int) -> tuple[Optional[Account], Optional[Share]]:
    account = Account.find(item)
    if account is None:
        return None, None

    if account.person == current_user.id:
        return account, None

    share = Share.find(account.folder, current_user.id)
    if share is None or share.confirmed is False:
        return respond_error(404)

    return account, share


def check_folder(
    folder: Optional[Folder], share: Optional[Share]
) -> Optional[Response]:
    if folder is None:
        return respond_error(400, "Folder could not be found.")

    if folder.person != current_user.id:
        if share is None or share.confirmed is False:
            return respond_error(400, "Folder could not be found.")

        if share.view_only is True:
            return respond_error(400, "No access to folder.")

    if len(Account.find_by_folder(folder.id)) >= 100:
        return respond_error(
            400, "Maximum number of accounts in folder is reached."
        )

    return None


@bp.get("/accounts")
@login_required
def get_accounts() -> Response:
    accounts = []

    shares = Share.find_by_person(current_user.id)

    for account in Account.find_by_person(current_user.id):
        share = next((x for x in shares if x.folder == account.folder), None)
        cipher = current_user.data_cipher(getattr(share, "secret", None))

        accounts.append(cipher.decrypt_account(account.to_dict()))

    return {"accounts": accounts}


@bp.post("/accounts")
@login_required
@parse_body(
    folder=fields.Str(required=True, validate=validate.Regexp("[0-9]+")),
    name=fields.Str(required=True, validate=validate.Length(1, 64)),
    username=fields.Str(required=True, validate=validate.Length(1, 256)),
    password=fields.Str(required=True, validate=validate.Length(1, 256)),
    note=fields.Str(required=True, validate=validate.Length(0, 1024)),
)
def post_accounts(body: dict) -> Response:
    folder = Folder.find(int(body["folder"]))
    share = Share.find(int(body["folder"]), current_user.id)

    error = check_folder(folder, share)
    if error is not None:
        return error

    cipher = current_user.data_cipher(getattr(share, "secret", None))
    body = cipher.encrypt_account(body)

    account = Account.create(
        person=current_user.id,
        folder=folder.id,
        name=body["name"],
        username=body["username"],
        password=body["password"],
        note=body["note"],
    )

    return cipher.decrypt_account(account.to_dict())


@bp.get("/accounts/<int:item>")
@login_required
def get_accounts_item(item: int) -> Response:
    account, share = get_account(item)
    if account is None:
        return respond_error(404)

    cipher = current_user.data_cipher(getattr(share, "secret", None))

    return cipher.decrypt_account(account.to_dict())


@bp.patch("/accounts/<int:item>")
@login_required
@parse_body(
    name=fields.Str(validate=validate.Length(1, 64)),
    username=fields.Str(validate=validate.Length(1, 256)),
    password=fields.Str(validate=validate.Length(1, 256)),
    note=fields.Str(validate=validate.Length(0, 1024)),
)
def patch_accounts_item(body: dict, item: int) -> Response:
    account, share = get_account(item)
    if account is None:
        return respond_error(404)

    if share and share.view_only is True:
        return respond_error(403)

    cipher = current_user.data_cipher(getattr(share, "secret", None))
    account.update(
        cipher,
        name=body.get("name"),
        username=body.get("username"),
        password=body.get("password"),
        note=body.get("note"),
    )

    return respond_default()


@bp.delete("/accounts/<int:item>")
@login_required
def delete_account_item(item: int) -> Response:
    account, share = get_account(item)
    if account is None:
        return respond_error(404)

    if share and share.view_only is True:
        return respond_error(403)

    account.delete()

    return respond_default()


@bp.put("/accounts/<int:item>/folder")
@login_required
@parse_body(
    folder=fields.Str(required=True, validate=validate.Regexp("[0-9]+")),
)
def put_account_item_folder(body: dict, item: int) -> Response:
    account, share = get_account(item)
    if account is None:
        return respond_error(404)

    if share and share.view_only is True:
        return respond_error(403)

    folder = Folder.find(int(body["folder"]))
    share = Share.find(int(body["folder"]), current_user.id)

    error = check_folder(folder, share)
    if error is not None:
        return error

    account.update_folder(current_user.secret_cipher(), folder.id)

    return respond_default()
