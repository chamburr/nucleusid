import math
import time
import uuid

from datetime import datetime

from server.utils import format_timestamp

EPOCH = 1609459200000


def generate() -> int:
    timestamp = math.floor(time.time() * 1000) - EPOCH
    random = uuid.uuid4().int & 0x3FFFFF

    return timestamp << 22 | random


def get_timestamp(snowflake: int) -> datetime:
    timestamp = EPOCH + (snowflake >> 22)
    return datetime.fromtimestamp(timestamp / 1000)


def get_iso_timestamp(snowflake: int) -> str:
    return format_timestamp(get_timestamp(snowflake))
