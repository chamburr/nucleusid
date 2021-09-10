from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from server import utils
from server.extensions import db, redis
from server.models import DeviceTable
from server.models.mixins import IdMixin
from server.utils import snowflake


class Device(DeviceTable, IdMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<Device id={self.id}>"

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "person": str(self.person),
            "name": self.name,
            "ip_address": self.ip_address,
            "location": self.location,
            "token_iat": self.token_iat,
            "last_login": utils.format_timestamp(self.last_login),
            "created_at": utils.format_timestamp(self.created_at),
        }

    @classmethod
    def create(
        cls,
        *,
        person: int,
        name: str,
        ip_address: str,
        location: str,
    ) -> Device:
        device = cls(
            id=snowflake.generate(),
            person=person,
            name=name,
            ip_address=ip_address,
            location=location,
            token_iat=0,
            last_login=datetime.now(),
        )

        db.session.add(device)
        db.session.commit()

        return device

    @classmethod
    def find(cls, identifier: int) -> Optional[Device]:
        return db.session.query(cls).get(identifier)

    @classmethod
    def find_by_person(cls, person: int) -> list[Device]:
        return db.session.query(cls).filter_by(person=person).all()

    def update(
        self,
        *,
        ip_address: Optional[str] = None,
        location: Optional[str] = None,
        token_iat: Optional[int] = None,
    ):
        if ip_address is not None:
            self.ip_address = ip_address

        if location is not None:
            self.location = location

        if token_iat is not None:
            redis.delete(f"device:{self.id}")
            self.token_iat = token_iat

        db.session.commit()

    def update_last_login(self):
        self.last_login = datetime.now()

        db.session.commit()

    def delete(self):
        redis.delete(f"device:{self.id}")

        db.session.delete(self)
        db.session.commit()

    @classmethod
    def delete_expired(cls):
        expiry = datetime.now() - timedelta(days=7)

        db.session.query(cls).filter(cls.last_login < expiry).delete()

        db.session.commit()
