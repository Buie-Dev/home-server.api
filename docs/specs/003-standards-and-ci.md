# 003 Standards and CI

## Goal

Add linting, formatting, CI, and clean up project config files so the repo follows consistent standards.

## Context

The repo has no linter, no formatter, no CI, and the .gitignore is a Bitbucket boilerplate with irrelevant entries (Java, Node, media files). There is no .env.example.

## Scope

- Add ruff config to pyproject.toml for lint and format
- Apply ruff format (pure formatting commit)
- Fix or suppress ruff lint errors (separate commit)
- Add .github/workflows/ci.yml running lint and tests on push/PR to main and dev
- Replace .gitignore with a Python-specific one covering .env and secrets/
- Add .env.example with all variables the code reads

## Out of scope

- Behavior changes
- New tests (baseline tests must pass unchanged)

## Acceptance criteria

- `ruff check .` passes with zero errors
- `ruff format --check .` passes with zero changes
- All 30 baseline tests still pass
- CI workflow is valid YAML
- .env.example lists every variable from config/config.py
- .gitignore covers .env, secrets/, __pycache__, .pytest_cache

## Test plan

- Run `ruff check .` and `ruff format --check .`
- Run `pytest` to confirm all 30 tests pass
- Validate CI YAML syntax

## Notes

- config/config.py line 36 prints DB credentials in get_db_config(). This is a Phase 6 fix.
- config/config.py line 24 will crash with TypeError if MQTT_PORT is not set. Phase 6 fix.
