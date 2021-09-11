from typing import Optional

from flask import Blueprint
from flask_login import current_user, login_required

from server.models.folder import Folder
from server.models.share import Share
from server.routes import Response, respond_default, respond_error

bp = Blueprint("shares", __name__)


def get_share(item: int) -> Optional[Share]:
    share = Share.find(item, current_user.id)
    if share is None:
        return None

    return share


@bp.get("/shares")
@login_required
def get_shares() -> Response:
    shares = []

    folders = Folder.find_by_person(current_user.id, confirmed=False)

    for share in Share.find_by_person(current_user.id):
        folder = next(x for x in folders if x.id == share.folder)

        share = share.to_dict()

        share["folder_name"] = folder.name

        del share["person"]
        del share["secret"]

        shares.append(share)

    return {"shares": shares}


@bp.get("/shares/<int:item>")
@login_required
def get_shares_item(item: int) -> Response:
    share = get_share(item)
    if share is None:
        return respond_error(404)

    folder = Folder.find(share.folder)

    share = share.to_dict()

    share["folder_name"] = folder.name

    del share["person"]
    del share["secret"]

    return share


@bp.post("/shares/<int:item>")
@login_required
def post_shares_item(item: int) -> Response:
    share = get_share(item)
    if share is None:
        return respond_error(404)

    if share.confirmed is True:
        respond_error(400, "Share is already confirmed.")

    if len(Folder.find_by_person(current_user.id)) >= 10:
        respond_error(400, "Maximum number of folders is reached.")

    share.update_confirmed()

    return respond_default()


@bp.delete("/shares/<int:item>")
@login_required
def delete_shares_item(item: int) -> Response:
    share = get_share(item)
    if share is None:
        return respond_error(404)

    if share.owner is True:
        return respond_error(400, "Owner share cannot be deleted.")

    share.delete()

    return respond_default()
