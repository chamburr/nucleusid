from typing import Callable, Optional, Union

from flask import abort
from webargs import flaskparser

Response = Union[tuple[dict, int], dict]


def respond(message: str) -> dict:
    return {"message": message}


def respond_default() -> dict:
    return {"message": "The request made is successful."}


def respond_error(
    code: int, message: Optional[str] = None, errors: Optional[dict] = None
) -> (dict, int):
    if message is None:
        abort(code)

    response = {"message": message}

    if errors is not None:
        response["errors"] = errors

    return response, code


parser = flaskparser.FlaskParser()


def parse_query(**kwargs) -> Callable[..., Callable]:
    return parser.use_args(kwargs, location="query", error_status_code=400)


def parse_body(**kwargs) -> Callable[..., Callable]:
    return parser.use_args(kwargs, location="json", error_status_code=400)
