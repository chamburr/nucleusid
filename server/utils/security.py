from __future__ import annotations

import base64
import hashlib

from calendar import timegm
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt

from flask import Request
from flask_login import UserMixin

from server.extensions import login
from server.models import person as _person
from server.models.device import Device
from server.utils import config
from server.utils.encryption import DataCipher, SecretCipher

#  TODO: Use Redis for caching
#  TODO: Update device table


class User(UserMixin):
    def __init__(
        self,
        token: str,
        iat: int,
        exp: int,
        person: _person.Person,
        device: Device,
        key: str,
    ):
        self.token = token
        self.iat = iat
        self.exp = exp
        self.person = person
        self.device = device
        self.key = key
        self.id = person.id

        self._secret_cipher = None
        self._data_cipher = None

    @classmethod
    def create(cls, person: _person.Person, device: Device, key: str) -> User:
        issued_at = datetime.utcnow()
        expires_at = issued_at + timedelta(days=7)

        issued_at = timegm(issued_at.utctimetuple())
        expires_at = timegm(expires_at.utctimetuple())

        device.update(token_iat=issued_at)

        token = jwt.encode(
            {
                "iat": issued_at,
                "exp": expires_at,
                "user": str(person.id),
                "device": str(device.id),
                "key": key,
            },
            config.SECRET_KEY,
            "HS256",
        )

        return User(token, issued_at, expires_at, person, device, key)

    @classmethod
    def from_token(cls, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                "HS256",
                {
                    "requires": ["iat", "exp", "user", "device", "key"],
                    "verify_iat": True,
                    "verify_exp": True,
                },
            )
        except jwt.PyJWTError:
            return None

        person = _person.Person.find(int(payload["user"]))
        if person is None:
            return None

        device = Device.find(int(payload["device"]))
        if device is None or device.token_iat != payload["iat"]:
            return None

        return User(
            token,
            payload["iat"],
            payload["exp"],
            person,
            device,
            payload["key"],
        )

    def verify_link(self) -> str:
        issued_at = datetime.utcnow()
        expires_at = issued_at + timedelta(days=1)

        issued_at = timegm(issued_at.utctimetuple())
        expires_at = timegm(expires_at.utctimetuple())

        token = jwt.encode(
            {
                "iat": issued_at,
                "exp": expires_at,
                "user": str(self.person.id),
                "email": self.person.email,
            },
            config.SECRET_KEY,
            "HS256",
        )

    def secret_cipher(self) -> SecretCipher:
        if self._secret_cipher is not None:
            return self._secret_cipher

        self._secret_cipher = SecretCipher.from_seed(self.key)

        return self._secret_cipher

    def data_cipher(self, secret: Optional[str] = None) -> DataCipher:
        if secret is not None:
            return DataCipher.from_key(self.secret_cipher().decrypt(secret))

        if self._data_cipher is not None:
            return self._data_cipher

        self._data_cipher = DataCipher.from_key(
            self.secret_cipher().decrypt(self.person.secret)
        )

        return self._data_cipher

    def refresh_token(self):
        user = User.create(self.person, self.device, self.key)
        self.token = user.token

    def logout(self):
        self.device.delete()


@login.request_loader
def load_user_from_request(request: Request) -> Optional[User]:
    token = request.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        return None

    token = token.replace("Bearer ", "", 1)

    user = User.from_token(token)
    if user is None:
        return None

    user.device.update_last_login()

    return user


def hash_password(password: str) -> str:
    password = base64.b64encode(hashlib.sha256(password.encode()).digest())
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password, salt).decode()


def check_password(password: str, hashed_password: str) -> bool:
    password = base64.b64encode(hashlib.sha256(password.encode()).digest())
    return bcrypt.checkpw(password, hashed_password.encode())
