from typing import Any, Dict, List, Optional
from flask_cors import CORS


from flasgger import Swagger
from flask import Flask, jsonify

from routes.IrrigationRoutes import irrigation

app = Flask(__name__)
Swagger(app)
CORS(app)
# Register blueprints
app.register_blueprint(irrigation, url_prefix="/irrigations")


@app.route("/", methods=["GET"])
def health_check() -> Any:
    return jsonify({"Status": "Connected"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
