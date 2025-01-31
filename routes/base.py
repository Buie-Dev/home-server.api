from typing import Any, Optional

from flask import jsonify


def formatReturn(data: Optional[Any]) -> Any:
    return jsonify(data)
