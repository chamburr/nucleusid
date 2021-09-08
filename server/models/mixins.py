from typing import TypeVar

from server.utils import snowflake

T = TypeVar("T")


class IdMixin:
    def __eq__(self: T, other: T) -> bool:
        return self.id == other.id

    def __hash__(self: T):
        return self.id >> 22

    @property
    def created_at(self: T):
        return snowflake.get_timestamp(self.id)
