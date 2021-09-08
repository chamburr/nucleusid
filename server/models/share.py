from __future__ import annotations

from datetime import datetime
from typing import Optional

from server import utils
from server.extensions import db
from server.models import ShareTable


class Share(ShareTable):
    def __repr__(self) -> str:
        return f"<Share folder={self.folder} person={self.person}>"

    def __str__(self) -> str:
        return f"{self.folder} {self.person}"

    def __eq__(self, other: Share) -> bool:
        return self.folder == other.folder and self.person == other.person

    def __hash__(self):
        return hash(f"{self.folder >> 22}:{self.person >> 22}")

    def to_dict(self) -> dict:
        return {
            "folder": str(self.folder),
            "person": str(self.person),
            "owner": self.owner,
            "view_only": self.view_only,
            "secret": self.secret,
            "confirmed": self.confirmed,
            "created_at": utils.format_timestamp(self.created_at),
        }

    @classmethod
    def create(
        cls,
        *,
        folder: int,
        person: int,
        view_only: bool,
        secret: str,
    ) -> Share:
        share = cls(
            folder=folder,
            person=person,
            owner=False,
            view_only=view_only,
            secret=secret,
            confirmed=False,
            created_at=datetime.now(),
        )

        db.session.add(share)
        db.session.commit()

        return share

    @classmethod
    def find(cls, folder: int, person: int) -> Optional[Share]:
        return db.session.query(cls).get((folder, person))

    @classmethod
    def find_by_folder(cls, folder: int) -> list[Share]:
        return db.session.query(cls).filter_by(folder=folder).all()

    @classmethod
    def find_by_person(cls, person: int) -> list[Share]:
        return db.session.query(cls).filter_by(person=person).all()

    def update(self, *, view_only: Optional[bool] = None):
        if not self.owner and view_only is not None:
            self.view_only = view_only

        db.session.commit()

    def update_confirmed(self):
        self.confirmed = True

        db.session.commit()

    def delete(self):
        if self.owner and len(Share.find_by_folder(self.folder)) > 1:
            return

        db.session.delete(self)
        db.session.commit()
