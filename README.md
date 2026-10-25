![CI](https://github.com/Buie-Dev/home-server.api/actions/workflows/ci.yml/badge.svg)

# home-server.api

Flask REST API that serves as the backend for my home automation and irrigation system.

## Why I built it

I needed a central API to manage irrigation schedules, zone configuration, and run history for my garden irrigation setup. The API connects everything together, letting my mobile app and web dashboard talk to the same data while MQTT handles real-time communication with the Raspberry Pi controllers out in the garden.

## How it fits

This is the REST API in a larger home automation system. The mobile app and web app send requests here, and the API coordinates with the MQTT broker to keep irrigation controllers in sync.

Related repos:

- [home-server.websocket](https://github.com/Buie-Dev/home-server.websocket) bridges WebSocket clients to MQTT for real-time updates
- [home-server.infra](https://github.com/Buie-Dev/home-server.infra) runs the shared infrastructure (MySQL, Mosquitto, nginx) via Docker Compose
- [irrigation-controller](https://github.com/Buie-Dev/irrigation-controller) manages the priority queue and relay timing on a Raspberry Pi
- [garden-controller](https://github.com/Buie-Dev/garden-controller) controls GPIO relays on a Raspberry Pi Zero 2W
- [irrigation-automation.service](https://github.com/Buie-Dev/irrigation-automation.service) triggers scheduled irrigations via MQTT

## Stack

- Python 3.9
- Flask with CORS and Flasgger (Swagger docs)
- PyMySQL with DBUtils connection pooling
- paho-mqtt for real-time schedule sync and health checks
- PyJWT and bcrypt for authentication
- Docker and Docker Compose

## Running it locally

Start the shared infrastructure first (MySQL, Mosquitto) from the home-server.infra repo.

```bash
# With Docker
docker compose up -d

# Without Docker
pip install -r requirements.txt
flask --app index run --host 0.0.0.0 --port 5001 --reload
```

The API will be available at `http://localhost:5001`. Hit `GET /` to confirm it's running.

## Configuration

Create a `.env` file in the repo root. See `.env.example` for the full list.

| Variable | Purpose |
|---|---|
| `API_MYSQL_HOST` | MySQL server hostname |
| `API_MYSQL_USERNAME` | MySQL username |
| `API_MYSQL_PASSWORD` | MySQL password |
| `API_MYSQL_DATABASE` | MySQL database name |
| `API_PORT` | MySQL port |
| `MQTT_BROKER` | MQTT broker hostname |
| `MQTT_PORT` | MQTT broker port |
| `MQTT_USERNAME` | MQTT username |
| `MQTT_PASSWORD` | MQTT password |
| `DEVICE_NAME` | Name reported in health check responses |
| `JWT_SECRET` | Secret key for signing JWT tokens |
| `APP_USERNAME` | Default app login username |
| `APP_PASSWORD_HASH` | Bcrypt hash of the app login password |

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests mock all external dependencies (MySQL, MQTT) so no running services are needed.

## How I work on it

Changes start as specs in `docs/specs/`. Claude Code implements them on a branch, and I review and merge every pull request.
