from calendar import timegm
from datetime import datetime, timedelta

import jwt

from flask import current_app

from server import utils
from server.extensions import mail
from server.models.device import Device
from server.models.person import Person
from server.models.share import Share
from server.utils import config


def get_verify_token(identifier: int, email: str) -> str:
    issued_at = datetime.utcnow()
    expires_at = issued_at + timedelta(days=1)

    issued_at = timegm(issued_at.utctimetuple())
    expires_at = timegm(expires_at.utctimetuple())

    token = jwt.encode(
        {
            "iat": issued_at,
            "exp": expires_at,
            "user": str(identifier),
            "email": email,
        },
        config.SECRET_KEY,
        "HS256",
    )

    return token


def send_register(person: Person):
    if config.MAIL_ENABLED is False:
        return

    token = get_verify_token(person.id, person.email)
    link = config.BASE_URI + "/verify?token=" + token

    message = current_app.jinja_env.get_template("register.jinja").render(
        name=person.name, link=link
    )

    mail.send_message(
        subject="Welcome to NucleusID", recipients=[person.email], body=message
    )


def send_verify(person: Person):
    if config.MAIL_ENABLED is False:
        return

    token = get_verify_token(person.id, person.email)
    link = f"{config.BASE_URI}/verify?token={token}"

    message = current_app.jinja_env.get_template("verify.jinja").render(
        name=person.name, link=link
    )

    mail.send_message(
        subject="Verify your NucleusID account",
        recipients=[person.email],
        body=message,
    )


def send_login(person: Person, device: Device):
    if config.MAIL_ENABLED is False:
        return

    timestamp = utils.format_timestamp(device.created_at)
    timestamp = timestamp.replace("T", " ").replace("Z", " (UTC)")

    message = current_app.jinja_env.get_template("login.jinja").render(
        name=person.name,
        timestamp=timestamp,
        device=device.name,
        location=device.location,
        ip_address=device.ip_address,
    )

    mail.send_message(
        subject="New login to NucleusID account",
        recipients=[person.email],
        body=message,
    )


def send_share(person: Person, inviter: Person, share: Share):
    if config.MAIL_ENABLED is False:
        return

    # todo: confirm link
    link = f"{config.BASE_URI}/dashboard/shares/{share.folder}"

    message = current_app.jinja_env.get_template("share.jinja").render(
        name=person.name,
        inviter=inviter.name,
        link=link,
    )

    mail.send_message(
        subject="Invitation to NucleusID folder",
        recipients=[person.email],
        body=message,
    )
