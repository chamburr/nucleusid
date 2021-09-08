from flask import Blueprint
from werkzeug.exceptions import (
    BadRequest,
    Forbidden,
    HTTPException,
    InternalServerError,
    MethodNotAllowed,
    NotFound,
    RequestTimeout,
    ServiceUnavailable,
    TooManyRequests,
    Unauthorized,
)

from server.routes import respond_error

bp = Blueprint("error", __name__)


@bp.app_errorhandler(BadRequest)
def bad_request(err: BadRequest) -> (dict, int):
    errors = err.data.get("messages", {}).get("json", {})
    errors |= err.data.get("messages", {}).get("query", {})

    return respond_error(
        err.code,
        "The request you made is invalid.",
        errors if len(errors) > 0 else None,
    )


@bp.app_errorhandler(Unauthorized)
def unauthorized(err: Unauthorized) -> (dict, int):
    return respond_error(
        err.code,
        "You are not authorised to access this resource.",
    )


@bp.app_errorhandler(Forbidden)
def forbidden(err: Forbidden) -> (dict, int):
    return respond_error(
        err.code,
        "You do not have permission to perform this action.",
    )


@bp.app_errorhandler(NotFound)
def not_found(err: NotFound) -> (dict, int):
    return respond_error(
        err.code,
        "The requested resource could not be found.",
    )


@bp.app_errorhandler(MethodNotAllowed)
def method_not_allowed(err: MethodNotAllowed) -> (dict, int):
    return respond_error(
        err.code,
        "The request method is not allowed for this resource.",
    )


@bp.app_errorhandler(RequestTimeout)
def request_timeout(err: RequestTimeout) -> (dict, int):
    return respond_error(
        err.code,
        "The server did not receive a complete request.",
    )


@bp.app_errorhandler(TooManyRequests)
def too_many_requests(err: TooManyRequests) -> (dict, int):
    return respond_error(
        err.code, "You have been rate limited, try again later."
    )


@bp.app_errorhandler(InternalServerError)
def internal_server_respond_error(err: InternalServerError) -> (dict, int):
    return respond_error(
        err.code,
        "The server encountered an internal respond_error.",
    )


@bp.app_errorhandler(ServiceUnavailable)
def service_unavailable(err: ServiceUnavailable) -> (dict, int):
    return respond_error(
        err.code,
        "The server cannot handle your request at this time.",
    )


@bp.app_errorhandler(HTTPException)
def http_exception(err: HTTPException) -> (dict, int):
    return respond_error(err.code, err.description)
