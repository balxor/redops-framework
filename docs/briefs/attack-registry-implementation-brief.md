# Brief for Codex — ATT&CK Registry & STIX Import

Status: Draft
Audience: Codex (backend implementation agent)
Related: `docs/attack-registry.md`, `docs/roadmap.md` (v0.2), `docs/data-model.md`
Owner sign-off required before merge: yes (security-sensitive content source)

---

## 1. Context

RedOps Framework is an ATT&CK-based platform. Every higher-level feature —
campaign planning, finding mapping, telemetry/detection review, reporting, and
LLM validation — depends on being able to resolve a real MITRE ATT&CK technique
by ID, know its tactic(s), platforms, data components, and whether it is
deprecated/revoked.

**Current state (placeholder):** `GET /api/v1/attack/techniques`
(`backend/app/api/v1/routes/attack.py`) returns two hardcoded techniques
(`T1059`, `T1046`) with `source="placeholder"`. There is no registry, no import,
and no persistence. The schema `app/schemas/attack.py` already signals this with
the `source` default of `"placeholder"`.

The frontend (`frontend/`) already consumes this endpoint and will render
whatever it returns — no frontend change is required once the endpoint serves
real data with the same (or a superset of the) response shape.

`docs/attack-registry.md` already specifies the intended model (entities,
source data, import metadata, domains). This brief asks Codex to turn that
draft spec into an implementation plan and then build it.

---

## 2. Objective

Replace the placeholder with a **local, version-aware ATT&CK Registry** populated
from **official MITRE ATT&CK STIX data**, starting with Enterprise.

Design principle (important): do **not** scrape or live-query `attack.mitre.org`
at request time. Import the official STIX/JSON dataset once, store it locally,
record provenance (source URL + content version + import timestamp), and serve
all lookups from the local store. This keeps engagements reproducible, offline-
capable, and pinned to a known ATT&CK version.

---

## 3. Source data

- Primary: MITRE ATT&CK STIX 2.1 bundle, `enterprise-attack.json`.
- Canonical origin: the official MITRE CTI distribution (record the exact
  `source_url` and `content_version`/spec version in the import log).
- Future (out of scope now, but model for it): `mobile-attack.json`,
  `ics-attack.json`. Keep `domain` explicit; never treat a technique from one
  domain as equivalent to another.

Licensing/attribution: MITRE ATT&CK is distributed under the ATT&CK Terms of
Use. Confirm attribution requirements and add a NOTICE/attribution line where
ATT&CK content is surfaced or redistributed.

---

## 4. Questions to decide first (Codex should propose answers)

1. **Import mechanism**: vendored dataset file committed to the repo vs. a
   fetch-on-deploy script vs. a CLI/management command run by an operator. Trade
   off reproducibility, repo size, and offline use. Recommend one.
2. **Parsing**: use `mitreattack-python` (official helper) vs. parse the STIX
   bundle directly. Note the dependency/footprint implication.
3. **Storage**: tables in the existing Postgres model (aligns with
   `docs/attack-registry.md` entities) vs. a read-only cached document. The doc
   leans relational — confirm and define the schema/migrations.
4. **Versioning**: how multiple ATT&CK content versions coexist, which is
   "active", and how existing mappings (findings/campaigns referencing a
   technique ID) behave when a technique is deprecated/revoked across versions.
5. **ID resolution & integrity**: should creating a finding/campaign step with
   an `attack_technique_id` validate against the registry? Hard fail, soft warn,
   or allow-with-flag? Tie this into the existing safety/validation approach.

---

## 5. Scope of work

In scope (v0.2):

- Registry persistence for, at minimum: `attack_collection`/import log,
  `attack_tactic`, `attack_technique` (incl. sub-techniques and the
  technique→tactic relationships), platforms, and `deprecated`/`revoked` flags.
- An idempotent import routine for `enterprise-attack.json` that writes an
  import-metadata record (`source_url`, `content_version`, `imported_at`,
  `object_count`, `status`).
- Replace the placeholder endpoint:
  - `GET /attack/techniques` — list/paginate/search by ID, name, tactic,
    platform; return `source` reflecting the real dataset version, not
    `"placeholder"`.
  - `GET /attack/techniques/{technique_id}` — single technique with tactics,
    platforms, data components, deprecation status, references.
  - (Optional) `GET /attack/tactics`.
- Keep the response shape backward-compatible with the current
  `AttackTechnique` schema (add fields, don't remove) so the frontend keeps
  working; extend `frontend/src/types/index.ts` only if new fields are added.

Out of scope (later versions): Mobile/ICS domains, groups/software/procedures,
ATT&CK Flow, and LLM mapping validation — model the schema so these can be added
without rework, but do not build them now.

---

## 6. Acceptance criteria

- Running the import against a pinned `enterprise-attack.json` populates the
  registry and records one import-log row with correct provenance.
- `GET /attack/techniques` returns real Enterprise techniques (hundreds, not 2),
  no `source="placeholder"` anywhere, and supports search/filter as above.
- Looking up a known ID (e.g. `T1059` and a sub-technique like `T1059.001`)
  returns correct tactic(s), platforms, and deprecation status.
- Re-running the import is idempotent (no duplicates) and a newer content
  version can be imported without corrupting existing data or mappings.
- Deprecated/revoked techniques are flagged, not silently dropped.
- Alembic migration(s) included; `pytest` covers import idempotency, ID lookup
  (including sub-technique), and the deprecated/revoked path.
- Attribution/NOTICE for MITRE ATT&CK content is present.

---

## 7. Notes & constraints

- Do not introduce live network calls on the request path; import is a separate,
  explicit step.
- Pin the ATT&CK content version; surface it in API responses and in generated
  reports so every engagement states which ATT&CK version it used.
- Coordinate with the existing safety model (`docs/safety-model.md`) for the
  technique-validation decision in §4.5.
- Frontend is ready and version-tolerant; ping if the response contract changes.

---

## 8. Deliverables

1. A short design note (answers to §4) appended to or alongside
   `docs/attack-registry.md`.
2. Migrations + models + import routine + updated endpoints.
3. Tests and attribution.
4. A line in `docs/roadmap.md` moving v0.2 ATT&CK registry from Planned to
   In progress/Done as appropriate.
