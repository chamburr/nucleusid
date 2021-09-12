import hashlib

from flask import Blueprint
from flask_login import current_user, login_required
from webargs import fields, validate

from server.extensions import limiter
from server.models.person import Person
from server.routes import Response, parse_body, respond_default, respond_error
from server.utils import mail, security

bp = Blueprint("user", __name__)


@bp.get("/user")
@login_required
def get_user() -> Response:
    person = current_user.person().to_dict()

    avatar = hashlib.md5(person["email"].lower().encode()).hexdigest()
    person["avatar"] = f"https://www.gravatar.com/avatar/{avatar}?d=retro"

    del person["password"]
    del person["public_key"]
    del person["secret"]

    return person


@bp.patch("/user")
@login_required
@parse_body(
    name=fields.Str(validate=validate.Length(1, 64)),
    email=fields.Email(validate=validate.Length(6, 256)),
)
def patch_user(body: dict) -> Response:
    person = current_user.person()

    if person.email == body.get("email", "").lower():
        del body["email"]

    if body.get("email") is not None:
        body["email"] = body["email"].lower()

        if Person.find_by_email(body["email"]) is not None:
            return respond_error(400, "Email is already registered.")

        mail.send_verify(person)

    person.update(
        name=body.get("name"),
        email=body.get("email"),
    )

    return respond_default()


@bp.delete("/user")
@login_required
@parse_body(
    password=fields.Str(required=True, validate=validate.Length(8, 128)),
)
def delete_user(body: dict) -> Response:
    person = current_user.person()

    if security.check_password(body["password"], person.password) is False:
        return respond_error(400, "Password is incorrect.")

    person.delete()

    return respond_default()


@bp.post("/user/resend_verify")
@limiter.limit("1/minute")
@login_required
def post_user_resend_verify() -> Response:
    person = current_user.person()

    if person.verified is True:
        return respond_error(400, "Email is already verified.")

    mail.send_verify(person)

    return respond_default()


@bp.put("/user/password")
@login_required
@parse_body(
    old_password=fields.Str(required=True, validate=validate.Length(8, 128)),
    password=fields.Str(required=True, validate=validate.Length(8, 128)),
)
def put_user_password(body: dict) -> Response:
    person = current_user.person()

    if security.check_password(body["old_password"], person.password) is False:
        return respond_error(400, "Old password is incorrect.")

    person.update_password(current_user.secret_cipher(), body["password"])

    return respond_default()
