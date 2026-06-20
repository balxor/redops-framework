# AGENTS.md

Guidance for AI coding agents (Codex, Claude, and similar) working in this
repository. Human contributors should read `CONTRIBUTING.md`; this file adds the
conventions and guardrails that matter specifically for autonomous agents.

---

## What this project is

RedOps Framework is an **ATT&CK-based platform for managing _authorized_ pentest
and red team operations** (scope, assets, campaigns, actions, evidence,
findings, reports, safety, telemetry, and LLM-assisted drafts). It is a
defensive, workflow-and-record system — **not** an exploitation or attack-
automation tool.

Read `docs/overview.md` and `docs/product-scope.md` before making non-trivial
changes.

---

## Hard safety boundaries (do not cross)

These mirror `docs/safety-model.md` and the Out-of-Scope lists in
`docs/product-scope.md` and `docs/roadmap.md`. An agent must **never** add,
scaffold, or "helpfully" stub:

- Autonomous exploitation, lateral movement, or privilege escalation
- Credential dumping/theft automation
- EDR/AV/defense bypass or evasion logic
- Malware, payload, C2, or phishing delivery
- Destructive testing or production execution without explicit authorization
- Any path that bypasses the Safety Gate or the approval workflow
- Direct command execution driven by an LLM without human approval

External tooling (Caldera, Atomic Red Team, scanners, SIEM/EDR) is **import-only**
and lab-first — see `docs/integrations.md`. If a task seems to require any of the
above, stop and ask a human maintainer instead of implementing it.

---

## Repository map

| Path             | What it is                                                        |
| ---------------- | ----------------------------------------------------------------- |
| `docs/`          | Source of truth for the model, scope, safety, and roadmap         |
| `docs/briefs/`   | Implementation briefs for agents (e.g. ATT&CK registry)           |
| `schemas/`       | JSON Schema for core entities                                     |
| `examples/`      | Sanitized example data — keep new examples sanitized              |
| `templates/`     | Document templates (finding, report, RoE, campaign)              |
| `backend/`       | FastAPI + SQLAlchemy + Alembic API (`backend/README.md`)          |
| `frontend/`      | React + Vite + TypeScript web console (`frontend/README.md`)      |

This repo is documentation-first: the `docs/` model leads, and code should
follow it. If code and docs disagree, surface the gap rather than silently
diverging.

---

## Working conventions

- **Check briefs first.** If a task matches a file in `docs/briefs/`, follow it
  and answer its open questions before coding.
- **Keep docs and code in sync.** Changing an API, schema, enum, or workflow
  means updating the relevant `docs/` file (and `frontend/src/types/` if the API
  contract changes).
- **Match existing style.** Docs use the `Status / Version / Project` header,
  `---` separators, and prose + tables. Backend mirrors the Pydantic schemas;
  frontend mirrors those schemas in `frontend/src/types/index.ts`.
- **Stay in scope.** Implement what the current roadmap version calls for; do not
  jump ahead to later-version features without being asked.
- **Sanitize everything public.** Examples, fixtures, and docs must not contain
  real targets, credentials, or client data. Use `example.com` / RFC 5737
  ranges (`192.0.2.0/24`, etc.).

---

## Verification expectations

Before declaring a change done:

- **Backend:** `python -m py_compile`, then run `pytest` in `backend/`. Add or
  update Alembic migrations for any model change.
- **Frontend:** `npm run build` (which runs `tsc -b && vite build`) must pass; no
  type errors.
- **Docs:** check internal links and that any new file is referenced from
  `README.md` and, where relevant, `docs/product-scope.md`.

State clearly what you verified and what you did not.

---

## Setup

See `docs/getting-started.md` for running the full stack locally.

---

## When unsure

Prefer asking a maintainer over guessing on: anything touching the safety model,
authorization, ATT&CK content sourcing/licensing, or external-tool execution.
For these, open an issue or leave a clearly marked TODO with the question rather
than implementing a risky default.
