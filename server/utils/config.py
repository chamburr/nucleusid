import os

from server.utils import build_url, parse_bool

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development").lower()

BASE_URI = os.environ.get("BASE_URI", "http://127.0.0.1")
SERVER_HOST = os.environ.get("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.environ.get("SERVER_PORT", "5000"))
SERVER_WORKERS = int(os.environ.get("SERVER_WORKERS", "4"))
SECRET_KEY = os.environ.get("SECRET_KEY", "secret")

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", "5432"))
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE", "nucleusid")

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
REDIS_DATABASE = int(os.getenv("REDIS_DATABASE", "0"))

MAIL_ENABLED = parse_bool(os.environ.get("MAIL_ENABLED", "false"))
MAIL_HOST = os.environ.get("MAIL_HOST", "127.0.0.1")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "25"))
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
MAIL_SENDER = os.environ.get("MAIL_SENDER", "test@example.com")
MAIL_SSL = parse_bool(os.environ.get("MAIL_SSL", "false"))

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")


def postgres_url() -> str:
    return build_url(
        "postgresql",
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_USERNAME,
        POSTGRES_PASSWORD,
        POSTGRES_DATABASE,
    )


def redis_url() -> str:
    return build_url(
        "redis",
        REDIS_HOST,
        REDIS_PORT,
        "",
        REDIS_PASSWORD,
        str(REDIS_DATABASE),
    )


flask_config = {
    "ENV": ENVIRONMENT,
    "JSON_SORT_KEYS": False,
    "SQLALCHEMY_DATABASE_URI": postgres_url(),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "RATELIMIT_APPLICATION": "10/second",
    "RATELIMIT_STORAGE_URL": redis_url(),
    "RATELIMIT_HEADERS_ENABLED": True,
    "MAIL_HOST": MAIL_HOST,
    "MAIL_PORT": MAIL_PORT,
    "MAIL_USERNAME": MAIL_USERNAME,
    "MAIL_PASSWORD": MAIL_PASSWORD,
    "MAIL_DEFAULT_SENDER": MAIL_SENDER,
    "MAIL_USE_SSL": MAIL_SSL,
    "REDIS_URL": redis_url(),
}
