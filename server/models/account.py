from __future__ import annotations

from typing import Optional

from server import utils
from server.extensions import db
from server.models import AccountTable
from server.models.mixins import IdMixin
from server.utils import snowflake
from server.utils.encryption import DataCipher, SecretCipher


class Account(AccountTable, IdMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<Account id={self.id}>"

    def __str__(self) -> str:
        return f"{self.name} {self.username}"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "person": str(self.person),
            "folder": str(self.folder),
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "totp": self.totp,
            "note": self.note,
            "created_at": utils.format_timestamp(self.created_at),
        }

    @classmethod
    def create(
        cls,
        *,
        person: int,
        folder: int,
        name: str,
        username: str,
        password: str,
        totp: str,
        note: str,
    ) -> Account:
        account = cls(
            id=snowflake.generate(),
            person=person,
            folder=folder,
            name=name,
            username=username,
            password=password,
            totp=totp,
            note=note,
        )

        db.session.add(account)
        db.session.commit()

        return account

    @classmethod
    def find(cls, identifier: int) -> Optional[Account]:
        return db.session.query(cls).get(identifier)

    @classmethod
    def find_by_person(cls, person: int) -> list[Account]:
        from server.models.share import Share

        shares = [
            x.folder
            for x in Share.find_by_person(person)
            if x.confirmed is True and x.owner is False
        ]

        return (
            db.session.query(cls)
            .filter((cls.person == person) | cls.folder.in_(shares))
            .all()
        )

    @classmethod
    def find_by_folder(cls, folder: int) -> list[Account]:
        return db.session.query(cls).filter_by(folder=folder).all()

    def update(
        self,
        cipher: DataCipher,
        *,
        name: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        totp: Optional[str] = None,
        note: Optional[str] = None,
    ):
        if name is not None:
            self.name = name

        if username is not None:
            self.username = username

        if password is not None:
            self.password = cipher.encrypt(password)

        if totp is not None:
            self.totp = cipher.encrypt(totp)

        if note is not None:
            self.note = note

        db.session.commit()

    def update_folder(self, secret_cipher: SecretCipher, folder: int):
        from server.models.person import Person
        from server.models.share import Share

        share = Share.find(self.folder, self.person)
        new_share = Share.find(folder, self.person)

        self.folder = folder

        if (share is None) is (new_share is None):
            db.session.commit()
            return

        person = Person.find(self.person)

        cipher = DataCipher.from_key(
            secret_cipher.decrypt(getattr(share, "secret", person.secret))
        )
        new_cipher = DataCipher.from_key(
            secret_cipher.decrypt(getattr(new_share, "secret", person.secret))
        )

        self.password = new_cipher.re_encrypt(cipher, self.password)
        self.totp = new_cipher.re_encrypt(cipher, self.totp)

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
