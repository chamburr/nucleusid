import jwt
import requests

from flask import Blueprint, request
from flask_login import current_user, login_required
from ua_parser import user_agent_parser
from webargs import fields, validate

from server.extensions import limiter
from server.models.device import Device
from server.models.person import Person
from server.routes import Response, parse_body, respond_default, respond_error
from server.utils import config, mail, security
from server.utils.encryption import SecretCipher
from server.utils.security import User

bp = Blueprint("auth", __name__)


@bp.post("/auth/register")
@limiter.limit("5/minute, 25/day")
@parse_body(
    name=fields.Str(required=True, validate=validate.Length(1, 64)),
    email=fields.Email(required=True, validate=validate.Length(6, 256)),
    password=fields.Str(required=True, validate=validate.Length(8, 256)),
)
def post_auth_register(body: dict) -> Response:
    body["email"] = body["email"].lower()

    if Person.find_by_email(body["email"]) is not None:
        return respond_error(400, "Email is already registered.")

    person = Person.create(
        name=body["name"],
        email=body["email"],
        password=body["password"],
    )

    mail.send_register(person)

    return respond_default()


@bp.post("/auth/login")
@limiter.limit("5/minute, 25/day")
@parse_body(
    email=fields.Email(required=True),
    password=fields.Str(required=True),
)
def post_auth_login(body: dict) -> Response:
    person = Person.find_by_email(body["email"])
    if person is None:
        return respond_error(400, "Email or password is invalid.")

    valid = security.check_password(body["password"], person.password)
    if valid is False:
        return respond_error(400, "Email or password is invalid.")

    agent = user_agent_parser.Parse(request.user_agent.string)
    name = f"{agent['user_agent']['family']} ({agent['os']['family']})"
    name = name.replace("Mac OS X", "macOS")

    ip = request.remote_addr
    geo = requests.get(f"https://geolocation-db.com/json/{ip}").json()
    location = f"{geo['city']}, {geo['country_name']}"
    location = location.replace("Not found", "Unknown")

    seed = SecretCipher.create(body["password"], person.id).seed

    device = Device.create(
        person=person.id, name=name, ip_address=ip, location=location
    )

    mail.send_login(person, device)

    user = User.create(person, device, seed)

    return {"token": user.token}


@bp.post("/user/verify")
@limiter.limit("5/minute, 25/day")
@parse_body(
    token=fields.Str(required=True),
)
def post_user_verify(body: dict) -> Response:
    try:
        payload = jwt.decode(
            body["token"],
            config.SECRET_KEY,
            "HS256",
            {
                "requires": ["iat", "exp", "user", "email"],
                "verify_iat": True,
                "verify_exp": True,
            },
        )
    except jwt.ExpiredSignatureError:
        return respond_error(400, "Verification token has expired.")
    except jwt.PyJWTError:
        return respond_error(400, "Verification token is invalid.")

    person = Person.find(int(payload["user"]))

    if person.verified:
        return respond_error(400, "Email is already verified.")

    if person.email != payload["email"]:
        return respond_error(400, "Verification token is invalid.")

    person.update_verified()

    return respond_default()


@bp.post("/auth/refresh")
@login_required
def post_auth_refresh() -> Response:
    current_user.refresh_token()

    return {"token": current_user.token}


@bp.post("/auth/logout")
@login_required
def post_auth_logout() -> Response:
    current_user.logout()

    return respond_default()
