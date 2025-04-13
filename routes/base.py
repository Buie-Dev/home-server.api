from typing import Any, Optional

from flask import jsonify, make_response


def format_return(data: Optional[Any]) -> Any:
    return jsonify(data)


def error_return(data: object, status_code: int) -> Any:
    return make_response(jsonify(data), status_code)
