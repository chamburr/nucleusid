from flask import Blueprint

from server.routes import respond_default

bp = Blueprint("index", __name__)


@bp.route("/")
def get_index() -> dict:
    return respond_default()
