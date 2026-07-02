from typing import Any, Dict, List, Optional
from flask_cors import CORS


from flasgger import Swagger
from flask import Flask, jsonify

from routes.IrrigationRoutes import irrigation
from routes.AuthRoutes import auth
from routes.DeviceRoutes import devices
from routes.MeganRoutes import megan
from routes.PeopleRoutes import people
from routes.AdminRoutes import admin
from routes.TodoRoutes import todo
from routes.EventRoutes import events

app = Flask(__name__)
Swagger(app)
CORS(app)
# Register blueprints
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(irrigation, url_prefix="/irrigations")
app.register_blueprint(devices, url_prefix="/devices")
app.register_blueprint(megan, url_prefix="/megan")
app.register_blueprint(people, url_prefix="/people")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(todo, url_prefix="/todo")
app.register_blueprint(events, url_prefix="/events")


@app.route("/", methods=["GET"])
def health_check() -> Any:
    return jsonify({"Status": "Connected"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
