from typing import Any, Dict, List, Optional

from flasgger import Swagger
from flask import Flask, jsonify

from routes.IrrigationRoutes import irrigation

app = Flask(__name__)
Swagger(app)
# Register blueprints
app.register_blueprint(irrigation, url_prefix="/irrigation")


@app.route("/", methods=["GET"])
def health_check() -> Any:
    return jsonify({"Status": "Connected"})


if __name__ == "__main__":
    app.run(debug=True)
