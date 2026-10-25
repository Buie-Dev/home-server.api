# 001 Project Setup

## Goal

Set up project documentation and contribution templates so the repo is easy to understand and contribute to.

## Context

This is a Flask REST API that serves as the backend for a home automation website and mobile app. It handles irrigation schedules, zones, history, device management, rowing, todos, events, and people. It connects to MySQL for data and MQTT for real-time communication. There are no existing docs (only a placeholder README), no spec templates, and no PR templates.

## Scope

- Create `CLAUDE.md` covering what the repo is and how it fits with related repos, stack and versions, commands to install/run/lint/test, folder layout, coding standards, ground rules, and the spec workflow.
- Create `docs/specs/000-template.md` with the standard spec sections.
- Create `.github/pull_request_template.md` with sections for Spec, What changed, How I tested it, What I checked by hand.

## Out of scope

- Adding tests, linters, or CI (later phases).
- Changing any application code.

## Acceptance criteria

- `CLAUDE.md` exists and accurately describes the repo.
- `docs/specs/000-template.md` exists with the standard sections.
- `.github/pull_request_template.md` exists with the required sections.

## Test plan

- Read each file and confirm it matches the requirements.

## Notes

None.
