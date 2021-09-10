from __future__ import annotations

from datetime import datetime
from typing import Optional

from server import utils
from server.extensions import db
from server.models import FolderTable
from server.models.mixins import IdMixin
from server.utils import snowflake
from server.utils.encryption import DataCipher, SecretCipher


class Folder(FolderTable, IdMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<Folder id={self.id}>"

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "person": str(self.person),
            "name": self.name,
            "sharing": self.sharing,
            "built_in": self.built_in,
            "created_at": utils.format_timestamp(self.created_at),
        }

    @classmethod
    def create(cls, *, person: int, name: str) -> Folder:
        folder = cls(
            id=snowflake.generate(),
            person=person,
            name=name,
            sharing=False,
            built_in=False,
        )

        db.session.add(folder)
        db.session.commit()

        return folder

    @classmethod
    def find(cls, identifier: int) -> Optional[Folder]:
        return db.session.query(cls).get(identifier)

    @classmethod
    def find_by_person(cls, person: int) -> list[Folder]:
        from server.models.share import Share

        shares = [
            x.folder
            for x in Share.find_by_person(person)
            if x.confirmed is True and x.owner is False
        ]

        return (
            db.session.query(cls)
            .filter((cls.person == person) | cls.id.in_(shares))
            .all()
        )

    def update(self, *, name: Optional[str] = None):
        if self.built_in is True:
            return

        if name is not None:
            self.name = name

        db.session.commit()

    def update_sharing(self, secret_cipher: SecretCipher, enabled: bool):
        from server.models.account import Account
        from server.models.person import Person
        from server.models.share import Share

        if self.built_in is True:
            return

        if self.sharing == enabled:
            return

        if enabled is True:
            person = Person.find(self.person)

            old_secret = secret_cipher.decrypt(person.secret)
            old_cipher = DataCipher.from_key(old_secret)
            cipher = DataCipher.create()

            self.sharing = True

            accounts = (
                db.session.query(Account).filter_by(folder=self.id).all()
            )
            for account in accounts:
                account.password = cipher.re_encrypt(
                    old_cipher, account.password
                )

            share = Share(
                folder=self.id,
                person=self.person,
                owner=True,
                view_only=False,
                secret=secret_cipher.encrypt(cipher.key),
                confirmed=True,
                created_at=datetime.now(),
            )

            db.session.add(share)
            db.session.commit()

            return

        person = Person.find(self.person)
        share = Share.find(self.id, self.person)

        old_secret = secret_cipher.decrypt(share.secret)
        old_cipher = DataCipher.from_key(old_secret)
        secret = secret_cipher.decrypt(person.secret)
        cipher = DataCipher.from_key(secret)

        self.sharing = False

        accounts = db.session.query(Account).filter_by(folder=self.id).all()
        for account in accounts:
            account.password = cipher.re_encrypt(old_cipher, account.password)

        db.session.query(Share).filter_by(folder=self.id).delete()

        db.session.commit()

    def delete(self):
        from server.models.account import Account
        from server.models.share import Share

        if self.built_in is True:
            return

        if Share.find_by_folder(self.id):
            return

        folder = (
            db.session.query(Folder)
            .filter_by(person=self.person, built_in=True)
            .one_or_none()
        )
        db.session.query(Account).filter_by(folder=self.id).update(
            {Account.folder: folder.id}
        )

        db.session.delete(self)
        db.session.commit()
