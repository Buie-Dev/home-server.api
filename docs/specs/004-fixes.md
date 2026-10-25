# 004 Fixes

## Goal

Fix bugs, remove debug prints, and clean up security issues identified during baseline testing.

## Context

Phase 4 baseline tests documented several bugs and code quality issues. This spec addresses them one fix at a time, each with a failing test first.

## Scope

### Debug prints (one commit)
Remove all `print()` calls from non-test code. These log credentials (config.py), query results (Base.py), request metadata (auth.py), and debug state (IrrigationServices.py, IrrigationRoutes.py, DeviceRoutes.py, IrrigationControllers.py). Replace error prints in routes with `logging.exception()` where the print is inside a catch block.

### Missing import (one commit)
`controllers/IrrigationControllers.py` uses `create_automation_command` but never imports it from `lib.irrigation`. Add the import and remove the noqa suppression.

### Swagger host mismatch (one commit)
`swagger.yaml` has `host: localhost:5000` but the API runs on port 5001. Fix to 5001.

## Out of scope

- `IrrigationModels.update_schedule()` calling `custom_delete()` instead of `custom_update()`. This needs careful manual testing against real data.
- `is_internal_ip` matching `172.` being overly broad. This is by design for Docker bridge networks.
- `.env` in git history. Already confirmed clean by gitleaks on full history.
- `ObjectTypes.py` duplicate `Subzone`. Both definitions are used in different contexts.

## Acceptance criteria

- Zero `print()` calls in non-test Python files
- `ruff check .` and `ruff format --check .` pass
- All 30 baseline tests pass
- `create_automation_command` is properly imported
- Swagger host matches port 5001

## Test plan

- `grep -r "print(" --include="*.py" --exclude-dir=tests` returns nothing
- `pytest` passes
- `ruff check .` passes

## Notes

- gitleaks found no leaks in the full git history
