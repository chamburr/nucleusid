from typing import Optional

from flask import Blueprint
from flask_login import current_user, login_required

from server.models.device import Device
from server.routes import Response, respond_default, respond_error

bp = Blueprint("devices", __name__)


def get_device(item: int) -> Optional[Device]:
    device = Device.find(item)
    if device is None or device.person != current_user.id:
        return None

    return device


@bp.get("/devices")
@login_required
def get_devices() -> Response:
    devices = []

    for device in Device.find_by_person(current_user.id):
        device = device.to_dict()
        del device["person"]
        del device["token_iat"]

        devices.append(device)

    return {"devices": devices}


@bp.get("/devices/<int:item>")
@login_required
def get_devices_item(item: int) -> Response:
    device = get_device(item)
    if device is None:
        return respond_error(404)

    device = device.to_dict()
    del device["person"]
    del device["token_iat"]

    return device


@bp.delete("/devices/<int:item>")
@login_required
def delete_devices_item(item: int) -> Response:
    device = get_device(item)
    if device is None:
        return respond_error(404)

    device.delete()

    return respond_default()
