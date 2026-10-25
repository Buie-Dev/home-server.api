# CLAUDE.md

## What this repo is

A Flask REST API that serves as the backend for my home automation website and mobile app. It handles irrigation schedules, zones, and run history, device management, rowing race tracking, todos with recurring automation, events, and people/contacts. It connects to MySQL for persistent data and to an MQTT broker for real-time communication with irrigation controllers and the automation service.

## How it fits

This is the central API in a larger home automation and irrigation system. Related repos:

- **home-server.websocket** — Python WebSocket server that bridges clients to MQTT
- **home-server.infra** — Docker Compose for shared infrastructure (MySQL, MongoDB, Mosquitto, nginx)
- **home-server.mobile** — React Native mobile app
- **home-server.web** — React web app
- **irrigation-controller** — Raspberry Pi service that manages the irrigation priority queue
- **garden-controller** — Raspberry Pi Zero 2W that controls GPIO relays
- **irrigation-automation.service** — Schedule runner that triggers irrigations via MQTT

All home server services join the shared Docker network defined in home-server.infra.

## Stack

- Python 3.9
- Flask with CORS and Flasgger (Swagger docs)
- PyMySQL with DBUtils connection pooling
- paho-mqtt (MQTT client for schedule sync and health checks)
- PyJWT and bcrypt (authentication)
- python-dotenv (environment config)
- Docker and Docker Compose

## Commands

```bash
# Run with Docker (production)
docker compose up -d

# Run locally (development)
pip install -r requirements.txt
flask --app index run --host 0.0.0.0 --port 5001 --reload

# Lint (after phase 5)
ruff check .
ruff format --check .

# Test (after phase 4)
pytest
```

## Folder layout

```
index.py                         Flask app entry point, blueprint registration
config/config.py                 Environment-based configuration
lib/auth.py                      JWT auth middleware (check_auth, check_user_auth)
lib/dates.py                     Vancouver timezone date helpers
lib/irrigation.py                Automation command builder
models/Base.py                   MySQL connection pool and query helpers
models/UserModels.py             User CRUD
models/PermissionsModels.py      Page permission management
models/IrrigationModels.py       Schedules, zones, subzones, history queries
models/DeviceModels.py           Device and battery queries
models/RowingModels.py           Rowing races, crews, boats, members queries
models/TodoModels.py             Todo tasks, templates, categories queries
models/EventModels.py            Events and categories queries
models/MeganModels.py            Ideas and categories queries
models/PeopleModels.py           People contacts and ideas queries
routes/AuthRoutes.py             Login, password, permissions endpoints
routes/AdminRoutes.py            User management endpoints
routes/IrrigationRoutes.py       Schedule, zone, history endpoints
routes/DeviceRoutes.py           Device and battery endpoints
routes/RowingRoutes.py           Rowing races, crews, boats, entries endpoints
routes/TodoRoutes.py             Todo tasks, templates, automation endpoints
routes/EventRoutes.py            Event CRUD endpoints
routes/MeganRoutes.py            Ideas CRUD endpoints
routes/PeopleRoutes.py           People and ideas endpoints
routes/base.py                   Response formatting helpers
controllers/                     Request handlers that call services
services/                        Business logic layer
mqtt/mqtt.py                     MQTT client with auto-reconnect
ObjectTypes.py                   TypedDict definitions
Dockerfile                       Python 3.9 container image
docker-compose.yaml              Service definition, joins home-server network
swagger.yaml                     Swagger 2.0 API spec
```

## Architecture

Routes → Controllers → Services → Models → MySQL. MQTT is used by controllers (to publish schedule changes) and by the mqtt module (to respond to health checks and sync requests).

Auth has two levels:
- `check_auth` — applied to all routes via `before_request`, allows internal IPs (192.168.1.*, 172.*, 127.*, 192.168.65.*) without a token
- `check_user_auth` — requires a valid JWT token regardless of IP, used on user-specific routes

## Environment variables

Defined in `.env` at the repo root, loaded by python-dotenv.

| Variable | Purpose | Example |
|---|---|---|
| `API_MYSQL_HOST` | MySQL server hostname | `mysql` |
| `API_MYSQL_USERNAME` | MySQL username | `root` |
| `API_MYSQL_PASSWORD` | MySQL password | (secret) |
| `API_MYSQL_DATABASE` | MySQL database name | `home` |
| `API_PORT` | MySQL port | `3306` |
| `MQTT_BROKER` | MQTT broker hostname | `mosquitto` |
| `MQTT_PORT` | MQTT broker port | `1883` |
| `MQTT_USERNAME` | MQTT username | `user` |
| `MQTT_PASSWORD` | MQTT password | (secret) |
| `DEVICE_NAME` | Name reported in health check responses | `homeserver_api` |
| `JWT_SECRET` | Secret key for signing JWT tokens | (random hex string) |
| `APP_USERNAME` | Default app login username | `admin` |
| `APP_PASSWORD_HASH` | Bcrypt hash of the app login password | (bcrypt hash) |

## Standards

- Two long-lived branches. `main` holds stable code, `dev` holds ongoing work. Spec branches are named `spec/NNN-short-name`, come off `dev`, and merge back into `dev`.
- Commit messages are imperative, sentence case, under 60 characters, no trailing period.
- Python uses ruff for lint and format, pytest for tests.
- `.gitignore` covers `.env` and `secrets/`.
- No secrets, real IPs, or credentials in committed code.

## Workflow

Changes start as specs in `docs/specs/`. Claude Code implements them on a spec branch, and I review and merge every pull request.

## Ground rules

- Never push to GitHub. I do all pushing.
- Never change app behavior unless a spec says to.
- Never commit `.env` files, secrets, real domains, real IP addresses, or hostnames.
- Never merge a pull request. I review and merge every one.
- Only write things that are true in the code.
