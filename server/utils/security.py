from __future__ import annotations

import base64
import hashlib

from calendar import timegm
from datetime import datetime, timedelta
from typing import Optional, Union

import bcrypt
import jwt

from flask import Request
from flask_login import UserMixin

from server.extensions import login, redis
from server.models import person as _person
from server.models.device import Device
from server.utils import config
from server.utils.encryption import DataCipher, SecretCipher


class User(UserMixin):
    def __init__(
        self,
        token: str,
        iat: int,
        exp: int,
        person: Union[_person.Person, int],
        device: Union[Device, int],
        secret: Optional[str],
        key: str,
    ):
        self.token = token
        self.iat = iat
        self.exp = exp
        self.key = key

        if isinstance(person, _person.Person):
            self._person = person
            self._person_id = person.id
            self._secret = person.secret
        else:
            self._person = None
            self._person_id = person
            self._secret = secret

        if isinstance(device, Device):
            self._device = device
            self._device_id = device.id
        else:
            self._device = None
            self._device_id = device

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

        return User(token, issued_at, expires_at, person, device, None, key)

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

        person = int(payload["user"])
        device = int(payload["device"])

        secret = redis.get(f"person:{person}")
        if secret is None:
            person = _person.Person.find(person)
            if person is None:
                return None

            secret = person.secret
            redis.set(f"person:{person.id}", secret)
            redis.expire(f"person:{person.id}", timedelta(hours=1))

        token_iat = redis.get(f"device:{device}")
        if token_iat is None:
            device = Device.find(device)
            if device is None:
                return None

            token_iat = str(device.token_iat)
            redis.set(f"device:{device.id}", token_iat)
            redis.expire(f"device:{device.id}", timedelta(hours=1))

        if token_iat != str(payload["iat"]):
            return None

        return User(
            token,
            payload["iat"],
            payload["exp"],
            person,
            device,
            secret,
            payload["key"],
        )

    @property
    def id(self) -> int:
        return self._person_id

    @property
    def device_id(self) -> int:
        return self._device_id

    def person(self) -> _person.Person:
        if self._person is None:
            self._person = _person.Person.find(self._person_id)

        return self._person

    def device(self) -> Device:
        if self._device is None:
            self._device = Device.find(self._device_id)

        return self._device

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
            self.secret_cipher().decrypt(self._secret)
        )

        return self._data_cipher

    def refresh_token(self):
        user = User.create(self.person(), self.device(), self.key)
        self.token = user.token

    def logout(self):
        self.device().delete()


@login.request_loader
def load_user_from_request(request: Request) -> Optional[User]:
    token = request.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        return None

    token = token.replace("Bearer ", "", 1)

    user = User.from_token(token)
    if user is None:
        return None

    device_login = redis.exists(f"device_login:{user.device_id}")
    if device_login is False:
        user.device().update_last_login()
        redis.set(f"device_login:{user.device_id}", "")
        redis.expire(f"device_login:{user.device_id}", timedelta(minutes=1))

    return user


def hash_password(password: str) -> str:
    password = base64.b64encode(hashlib.sha256(password.encode()).digest())
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password, salt).decode()


def check_password(password: str, hashed_password: str) -> bool:
    password = base64.b64encode(hashlib.sha256(password.encode()).digest())
    return bcrypt.checkpw(password, hashed_password.encode())
