# Integrations

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This document defines how RedOps Framework integrates with external security
tooling. It expands the `external_tool_import`, `siem_integration`,
`edr_integration`, and `controlled_runner_interface` items listed under Future
Scope in `docs/product-scope.md`, and the External tool import / Detection
engineering integration items in `docs/roadmap.md`.

Integrations exist to enrich the engagement record — campaign planning, action
logging, evidence, finding mapping, and detection feedback — not to add
offensive capability to the framework itself.

---

## Integration Principles

All integrations follow the same safety-first rules as the rest of the
framework (`docs/safety-model.md`):

1. **Import over execute.** Default integration direction is *inbound*: pull
   results, definitions, or telemetry into the framework. The framework is the
   system of record, not an attack launcher.
2. **No autonomous offense.** The framework never auto-executes adversary
   actions. Any execution stays manual or operator-triggered, gated by approval,
   and lab-first.
3. **Scope-bound.** Imported data is attached to a project and validated against
   the approved scope. Out-of-scope artifacts are flagged, not silently stored.
4. **Human gate for any run.** If an integration can trigger activity (e.g. an
   emulation plan), it must pass the Safety Gate and require approval for
   restricted steps.
5. **Provenance.** Every import records source tool, version, source file/URL,
   importer, and timestamp, mirroring the ATT&CK registry import-log pattern.
6. **Sanitization.** Imported evidence and logs follow the same sanitization
   expectation as manually uploaded evidence.

---

## Integration Categories

| Category                 | Direction | Example tools                         | Primary use                                              |
| ------------------------ | --------- | ------------------------------------- | -------------------------------------------------------- |
| Adversary emulation      | Import    | MITRE Caldera, Atomic Red Team        | Map planned/executed campaign steps to ATT&CK techniques |
| Vulnerability scanners   | Import    | Nuclei, generic scanner output        | Seed findings and assets from authorized scan results    |
| Web proxy / DAST         | Import    | Burp Suite export                     | Attach request/response evidence to actions and findings |
| Detection sources        | Import    | SIEM, EDR alerts and queries          | Record detection feedback and telemetry status           |
| ATT&CK content           | Import    | MITRE ATT&CK STIX                     | Populate the ATT&CK registry (see `attack-registry.md`)  |

---

## Adversary Emulation (Caldera, Atomic Red Team)

### Intent

Adversary-emulation tooling describes attacker behaviors that are already mapped
to ATT&CK. RedOps consumes those mappings to plan campaigns and to reconcile
planned vs. executed vs. detected activity. RedOps does **not** become a Caldera
controller or ship Atomic test payloads.

### Atomic Red Team

- **What it is:** a library of small, ATT&CK-mapped test definitions.
- **Integration:** import test *definitions* (technique ID, name, supported
  platforms, description) to pre-fill campaign steps and the technique browser.
  Operators still execute any test manually in an authorized lab and record the
  result as an Action with linked Evidence.
- **In scope:** definition import, technique mapping, step templating.
- **Out of scope:** automatic execution of atomics from the framework.

### MITRE Caldera

- **What it is:** an automated adversary-emulation platform with ATT&CK-mapped
  abilities and operations.
- **Integration (later, optional):** import Caldera *operation reports* (which
  abilities ran, against which host, with which ATT&CK technique) to populate the
  Operation Timeline and Detection Feedback after an authorized exercise.
- **In scope:** read-only import of operation results and ability metadata.
- **Out of scope (for now):** the framework orchestrating Caldera operations.
  If a controlled runner interface is ever added (`v0.6+`), it must sit behind
  the Safety Gate, approval workflow, and lab-first policy.

---

## Vulnerability Scanners & DAST (Nuclei, Burp, generic)

- **Nuclei / scanner import:** parse authorized scan output into draft findings
  and asset records. Imported findings start in `draft`/`under_review` and must
  be confirmed by an operator/reviewer before they count as confirmed findings.
- **Burp export:** attach HTTP request/response pairs as evidence linked to an
  action or finding. Treat exported items as sensitive; apply sanitization.
- **Mapping:** where the tool provides a CWE/ATT&CK hint, surface it as a
  *suggested* ATT&CK mapping for operator confirmation — never auto-confirmed.

---

## Detection Sources (SIEM / EDR)

- **Direction:** import alerts and, optionally, the result of an operator-run
  query. The framework records detection feedback; it does not run live queries
  on the request path and does not deploy detection rules.
- **Use:** link a SIEM/EDR alert to a campaign step or action to set a
  `detection_status` (`detected`, `not_detected`, `blocked`,
  `partially_detected`, `not_applicable`) per `docs/telemetry-model.md`.
- **Out of scope (early):** direct SIEM/EDR query execution, rule deployment,
  and detection-engineering CI/CD (already listed as excluded in
  `product-scope.md` → Telemetry Model).

---

## Import Provenance Model

Every integration import should record:

```text
import_id
integration_type        (adversary_emulation | scanner | dast | detection | attack_stix)
source_tool             (e.g. caldera, atomic_red_team, nuclei, burp, splunk)
source_tool_version
source_file_or_url
project_id
imported_by
imported_at
object_count
status                  (pending | imported | partial | failed)
notes
```

---

## Roadmap Alignment

| Capability                         | Stage (roadmap)                         |
| ---------------------------------- | --------------------------------------- |
| ATT&CK STIX import                 | v0.2 (ATT&CK registry)                  |
| Scanner / Burp / Nuclei import     | Long-term — External tool import        |
| Atomic Red Team definition import  | Long-term — External tool import        |
| SIEM / EDR detection feedback      | v0.7 + Detection engineering integration|
| Caldera operation-report import    | After controlled runner interface (v0.6+)|
| Controlled runner interface        | v0.6 (safe validation workflow)         |

---

## Out of Scope

Consistent with `docs/roadmap.md` and `docs/safety-model.md`, integrations must
never add:

* Autonomous exploitation or lateral movement
* Credential dumping automation
* EDR or AV bypass automation
* Malware, payload, or phishing delivery
* Destructive testing
* Production execution without explicit authorization
* Any execution path that bypasses the Safety Gate or approval workflow

---

## Status

Current status:

```text
v0.1 — design draft, no integration implemented yet
```

This document defines intent and boundaries. Implementation follows the roadmap
and must be reviewed against the safety model before any integration is built.
