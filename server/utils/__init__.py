from datetime import datetime, timezone
from typing import Callable, Optional

from flask import Flask


def with_context(app: Flask, func: Callable) -> Callable:
    def function():
        with app.app_context():
            func()

    return function


def format_timestamp(timestamp: datetime) -> str:
    timestamp = timestamp.astimezone(timezone.utc).replace(microsecond=0)
    return timestamp.isoformat().replace("+00:00", "Z")


def parse_bool(s: str) -> bool:
    if s.strip().lower() in ("yes", "true", "on", "1"):
        return True
    return False


def build_url(
    scheme: str,
    host: str,
    port: Optional[int] = None,
    username: Optional[str] = "",
    password: Optional[str] = "",
    path: Optional[str] = "",
) -> str:
    if port:
        host += f":{port}"

    if password:
        username += f":{password}"

    if username:
        username += "@"

    if path and not path.startswith("/"):
        path = f"/{path}"

    return f"{scheme}://{username}{host}{path}"
