from __future__ import annotations

from datetime import datetime
from typing import Optional

from server import utils
from server.extensions import db, redis
from server.models import PersonTable
from server.models.mixins import IdMixin
from server.utils import security, snowflake
from server.utils.encryption import DataCipher, SecretCipher


class Person(PersonTable, IdMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<Person id={self.id}>"

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "public_key": self.public_key,
            "secret": self.secret,
            "verified": self.verified,
            "updated_at": utils.format_timestamp(self.updated_at),
            "created_at": utils.format_timestamp(self.created_at),
        }

    @classmethod
    def create(cls, *, name: str, email: str, password: str) -> Person:
        from server.models.folder import Folder

        identifier = snowflake.generate()

        cipher = SecretCipher.create(password, identifier)
        secret = cipher.encrypt(DataCipher.create().key)

        person = cls(
            id=identifier,
            name=name,
            email=email,
            password=security.hash_password(password),
            public_key=cipher.public_key,
            secret=secret,
            verified=False,
            updated_at=datetime.now(),
        )

        folder = Folder(
            id=snowflake.generate(),
            person=identifier,
            name="Default",
            sharing=False,
            built_in=True,
        )

        db.session.add(person)
        db.session.add(folder)
        db.session.commit()

        return person

    @classmethod
    def find(cls, identifier: int) -> Optional[Person]:
        return db.session.query(cls).get(identifier)

    @classmethod
    def find_by_email(cls, email: str) -> Optional[Person]:
        return db.session.query(cls).filter_by(email=email).one_or_none()

    def update(
        self, *, name: Optional[str] = None, email: Optional[str] = None
    ):
        if name is not None:
            self.name = name

        if email is not None:
            self.email = email
            self.verified = False

        db.session.commit()

    def update_verified(self):
        self.verified = True

        db.session.commit()

    def update_password(self, old_cipher: SecretCipher, password: str):
        from server.models.device import Device
        from server.models.share import Share

        cipher = SecretCipher.create(password, self.id)

        self.password = security.hash_password(password)
        self.public_key = cipher.public_key
        self.secret = cipher.re_encrypt(old_cipher, self.secret)

        shares = db.session.query(Share).filter_by(person=self.id).all()
        for share in shares:
            share.secret = cipher.re_encrypt(old_cipher, Share.secret)

        redis.delete(f"person:{self.id}")

        devices = Device.find_by_person(self.id)
        redis.delete(*(f"device:{x.id}" for x in devices))

        db.session.query(Device).filter_by(person=self.id).delete()

        db.session.commit()

    def delete(self):
        from server.models.account import Account
        from server.models.device import Device
        from server.models.folder import Folder
        from server.models.share import Share

        redis.delete(f"person:{self.id}")

        devices = Device.find_by_person(self.id)
        redis.delete(*(f"device:{x.id}" for x in devices))

        db.session.query(Account).filter_by(person=self.id).delete()
        db.session.query(Device).filter_by(person=self.id).delete()
        db.session.query(Share).filter_by(person=self.id).delete()
        db.session.query(Folder).filter_by(person=self.id).delete()

        db.session.delete(self)
        db.session.commit()
