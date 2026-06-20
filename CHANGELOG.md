# Changelog

All notable changes to RedOps Framework are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project aims to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Versions track the stages defined in `docs/roadmap.md`.

---

## [Unreleased]

### Added

- Web console (`frontend/`): React + Vite + TypeScript + Tailwind + TanStack
  Query client over the API, with auth, dashboard, projects, project detail
  tabs, users, and ATT&CK reference views.
- `docs/integrations.md` — design for external tooling integration (MITRE
  Caldera, Atomic Red Team, scanners/DAST, SIEM/EDR), import-only and lab-first.
- `docs/getting-started.md` — full-stack local setup (backend + frontend + DB).
- `AGENTS.md` — conventions and safety guardrails for AI coding agents.
- `docs/briefs/` — implementation briefs for agents, starting with the ATT&CK
  registry & STIX import brief.
- Operating Modes (Pentest Mode / Red Team Mode) framing in
  `docs/product-scope.md`.

### Changed

- `README.md`, `docs/architecture.md`, and `docs/roadmap.md` now reference the
  implemented frontend stack (React + Vite) and the web console.

### Notes

- ATT&CK technique data remains a placeholder (`/attack/techniques` returns a
  stub) until the ATT&CK registry / STIX import is implemented.

---

## [0.1.0] — 2026-06

Initial community draft (documentation-first), per roadmap v0.1.

### Added

- Repository structure: `README.md`, `LICENSE`, `SECURITY.md`,
  `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, GitHub issue/PR templates.
- Documentation set in `docs/` (overview, product scope, architecture, ATT&CK
  registry, safety model, telemetry model, LLM assistance, data model, API,
  roadmap, glossary).
- `schemas/`, `examples/`, `templates/`, and `diagrams/` starter content.
- Backend API skeleton (`backend/`): FastAPI + SQLAlchemy + Alembic with
  projects, scopes, assets, campaigns, actions, evidence, findings, reports,
  members, safety summary, JWT auth, RBAC, and an ATT&CK technique placeholder.

[Unreleased]: https://github.com/
[0.1.0]: https://github.com/
