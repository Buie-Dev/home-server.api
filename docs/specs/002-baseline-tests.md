# 002 Baseline Tests

## Goal

Add tests that lock in how the code behaves today, before any other changes.

## Context

The API has a layered architecture (routes → controllers → services → models) with JWT/IP authentication, MySQL queries via a connection pool, and MQTT integration. All external dependencies (MySQL, MQTT broker, HTTP requests) must be mocked. The most important behavior to test is the auth middleware, service-layer business logic, and MQTT integration.

## Scope

- Add pytest as the test framework with config in `pyproject.toml` and `requirements-dev.txt`.
- Add `conftest.py` with shared fixtures (Flask test client, patched Config, mock DB).

### Auth tests (lib/auth.py)
- `check_auth` allows internal IPs without token.
- `check_auth` requires valid JWT for external IPs.
- `check_auth` rejects expired and invalid tokens.
- `check_user_auth` always requires a valid token regardless of IP.

### Irrigation service tests (services/IrrigationServices.py)
- Schedule formatting and creation logic.
- Automation command building (lib/irrigation.py).
- History litres calculation with subzone splitting.

### MQTT tests (mqtt/mqtt.py)
- Health check request triggers a response publish.
- Schedule status request triggers status publish.
- Auto-reconnect callbacks are wired correctly.

### Route smoke tests
- Health check endpoint returns 200.
- Auth-protected endpoints return 401 without token.

### Mock all external dependencies
- MySQL via patching Base query methods.
- MQTT via patching the mqtt_client.
- No test may need real databases or services.

## Out of scope

- Changing any application code.
- Testing every endpoint (focus on behavior that matters most).
- Integration tests requiring real MySQL or MQTT.

## Acceptance criteria

- `pytest` runs and all tests pass.
- All external dependencies are mocked.
- No application code is changed.

## Test plan

- Run `pytest -v` and confirm all tests pass.

## Notes

Likely bugs to investigate in Phase 6:
- `config.py` `get_db_config()` prints database credentials to stdout.
- `Base.py` prints query results and row counts on every operation.
- `lib/auth.py` prints the request remote address on every request.
- `IrrigationServices.py` has debug prints (lines 147-149).
- `ObjectTypes.py` defines `Subzone` twice with different structures.
- `swagger.yaml` has `host: localhost:5000` but API runs on port 5001.
- `.env` was committed in history with real passwords, IPs, and JWT secret.
- `IrrigationModels.update_schedule()` calls `Base.custom_delete()` instead of `custom_update()`.
- `is_internal_ip` matching `172.` is overly broad (same as websocket repo).
