from typing import Any, Dict, List, Optional

from flask import Blueprint, Flask, jsonify, request

from controllers.IrrigationControllers import IrrigationControllers
from routes.base import formatReturn

irrigation = Blueprint("irrigation", __name__)


@irrigation.route("/schedules", methods=["GET"])
def schedules() -> Any:
    data = IrrigationControllers.schedules()
    print(data)
    return formatReturn(data)
