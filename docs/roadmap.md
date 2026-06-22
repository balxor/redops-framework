# Roadmap

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This roadmap defines the planned development sequence for RedOps Framework.

The project starts as a documentation-first framework. Implementation work should follow after the core model, safety rules, data structure, and workflow are reviewed.

---

## Version Plan

| Version | Focus                                           | Status      |
| ------- | ----------------------------------------------- | ----------- |
| v0.1    | Community draft and repository structure        | In progress |
| v0.2    | ATT&CK registry and data model                  | Planned     |
| v0.3    | Campaign, action, evidence, and finding model   | Planned     |
| v0.4    | Safety gate, approval workflow, and audit model | Planned     |
| v0.5    | LLM-assisted workflow model                     | Planned     |
| v0.6    | Safe validation workflow model                  | Planned     |
| v0.7    | Telemetry model and detection feedback          | Planned     |
| v1.0    | Stable framework specification                  | Planned     |

---

## v0.1 Community Draft

### Scope

v0.1 defines the public structure of the project.

### Deliverables

* `README.md`
* `SECURITY.md`
* `CONTRIBUTING.md`
* `CODE_OF_CONDUCT.md`
* Initial `docs/` structure
* Initial `schemas/` structure
* Initial `examples/` structure
* Initial `templates/` structure
* Initial `diagrams/` structure
* Initial GitHub issue templates
* Initial pull request template

### Completion Criteria

v0.1 is complete when:

* The repository has a clear README.
* The security policy is documented.
* The contribution process is documented.
* The roadmap is documented.
* The safety model has an initial draft.
* The LLM assistance model has an initial draft.
* The architecture overview has an initial draft.

---

## v0.2 ATT&CK Registry and Data Model

### Scope

v0.2 defines how ATT&CK data is represented inside the framework.

### Deliverables

* `docs/attack-registry.md`
* `docs/data-model.md`
* ATT&CK tactic model
* ATT&CK technique model
* ATT&CK sub-technique model
* ATT&CK relationship model
* Version-aware registry design
* STIX import design
* Initial JSON schema drafts

### Completion Criteria

v0.2 is complete when:

* ATT&CK entities are defined.
* ATT&CK version handling is documented.
* STIX import behavior is described.
* Data relationships are documented.
* JSON schema drafts exist for core entities.

---

## v0.3 Campaign, Action, Evidence, and Finding Model

### Scope

v0.3 defines the main engagement workflow.

### Deliverables

* Campaign model
* Campaign step model
* Action log model
* Evidence model
* Finding model
* Report outline model
* Example campaign file
* Example finding file
* Example report outline
* Templates for campaign plan, finding, and report

### Completion Criteria

v0.3 is complete when:

* A campaign can be represented as structured data.
* A campaign step can reference an ATT&CK technique.
* An action can be linked to a campaign step.
* Evidence can be linked to an action or finding.
* A finding can be linked to an asset, evidence, and ATT&CK technique.
* A report outline can be generated from project data.

---

## v0.4 Safety Gate, Approval Workflow, and Audit Model

### Scope

v0.4 defines control requirements for authorized use.

### Deliverables

* `docs/safety-model.md`
* Scope validation rules
* Target allowlist rules
* Restricted action policy
* Approval workflow
* Audit event model
* Evidence integrity requirements
* Role and permission model
* Safety review checklist

### Completion Criteria

v0.4 is complete when:

* Scope validation is documented.
* Restricted actions are classified.
* Approval workflow is defined.
* Audit events are defined.
* Evidence integrity requirements are defined.
* Role-based access requirements are defined.

---

## v0.5 LLM-Assisted Workflow Model

### Scope

v0.5 defines how LLM support can be used in the framework.

### Supported LLM Functions

* Scope summary
* ATT&CK mapping suggestion
* Campaign plan draft
* Policy review
* Evidence summary
* Finding draft
* Remediation draft
* Report draft
* Telemetry gap analysis
* Cleanup checklist

### Deliverables

* `docs/llm-assistance.md`
* LLM role definition
* LLM input and output boundaries
* Structured plan draft format
* Validation requirements
* Human approval requirements
* Prompt safety rules
* LLM review checklist

### Completion Criteria

v0.5 is complete when:

* LLM-supported tasks are documented.
* LLM-restricted tasks are documented.
* LLM output validation is defined.
* LLM-generated plans require policy validation.
* LLM-generated plans require human approval before execution.

---

## v0.6 Safe Validation Workflow Model

### Scope

v0.6 defines controlled validation workflow concepts.

### Deliverables

* Safe validation workflow format
* Controlled runner interface proposal
* External tool import design (`docs/integrations.md`)
* Adversary-emulation import design (Atomic Red Team, MITRE Caldera — import only)
* Lab-first validation policy
* Cleanup and revert requirements
* Validation status model
* Example safe workflow file

### Completion Criteria

v0.6 is complete when:

* Safe validation workflows are represented as structured plans.
* Workflow execution requirements are documented.
* Cleanup requirements are documented.
* Revert requirements are documented.
* External tool import boundaries are documented.

---

## v0.7 Telemetry Model and Detection Feedback

### Scope

v0.7 defines how detection feedback and telemetry review are represented.

### Deliverables

* `docs/telemetry-model.md`
* Expected telemetry model
* Observed telemetry model
* Detection status values
* Telemetry gap model
* Detection feedback workflow
* ATT&CK data component mapping
* Report section for detection feedback

### Detection Status Values

```text
unknown
detected
not_detected
blocked
partially_detected
not_applicable
```

### Completion Criteria

v0.7 is complete when:

* Expected telemetry can be mapped to a campaign step.
* Observed telemetry can be linked to evidence.
* Detection status can be recorded.
* Detection gap can be described.
* Detection feedback can be included in reports.

---

## v1.0 Stable Framework Specification

### Scope

v1.0 defines the first stable specification of RedOps Framework.

### Deliverables

* Complete README
* Complete documentation set
* Complete schema set
* Complete template set
* Complete example set
* Stable terminology
* Stable safety model
* Stable roadmap
* Contribution process
* Security policy

### Completion Criteria

v1.0 is complete when:

* The framework can be reviewed as a complete specification.
* The documentation is consistent across files.
* The data model is stable enough for implementation planning.
* The safety model is defined.
* LLM-assisted workflow boundaries are defined.
* The project can accept external contribution with clear rules.

---

## Implementation Phase

Implementation has started alongside the documentation model. Current code
includes a FastAPI backend, SQLAlchemy/Alembic persistence, Docker Compose,
and a React + Vite frontend console for the core workflow.

Suggested implementation sequence:

1. Backend API foundation — implemented
2. Database schema — implemented
3. Project and scope module — implemented
4. Asset registry — implemented
5. ATT&CK registry lookup — implemented as a local reference catalog
6. Campaign planner — implemented
7. Action log — implemented
8. Evidence metadata vault — implemented
9. Finding manager — implemented
10. Report builder outline generation — implemented
11. Safety gate — implemented for approved scope, allowlist, and approvals
12. Web console (React + Vite frontend, see `frontend/`) — implemented
13. LLM-assisted draft review — implemented as review-gated records
14. Telemetry feedback — implemented
15. Safe validation workflow — future scope

---

## Implementation Stack Proposal

| Area          | Suggested Technology                                  |
| ------------- | ----------------------------------------------------- |
| Backend       | Python, FastAPI                                       |
| Database      | PostgreSQL                                            |
| ORM           | SQLAlchemy                                            |
| Migration     | Alembic                                               |
| Frontend      | React + Vite + TypeScript (implemented in `frontend/`) |
| UI            | Tailwind CSS                                          |
| Data fetching | TanStack Query                                        |
| Storage       | Local filesystem for MVP, S3-compatible storage later |
| Auth          | JWT for MVP, SSO later                                |
| Documentation | Markdown                                              |
| Diagrams      | Mermaid                                               |
| Schema        | JSON Schema                                           |

---

## Priority Order

Short-term priority:

1. Documentation consistency
2. Safety model
3. Data model
4. ATT&CK registry model
5. LLM assistance boundaries
6. Example files
7. Templates

Mid-term priority:

1. Backend implementation plan
2. API contract
3. Database schema
4. UI workflow
5. Report builder design
6. Evidence handling design

Long-term priority:

1. Safe validation workflow
2. External tool import — scanners, DAST, adversary emulation (`docs/integrations.md`)
3. Telemetry feedback
4. Detection engineering integration — SIEM/EDR detection feedback
5. Multi-project workspace
6. Role and permission expansion

---

## Out of Scope for Early Versions

The following items are not planned for early versions:

* Autonomous exploitation
* Autonomous lateral movement
* Credential dumping automation
* EDR or AV bypass automation
* Malware generation
* Payload delivery
* Phishing delivery
* Destructive testing
* Production execution without explicit authorization
* Direct command execution by LLM without approval

---

## Review Checklist

Before moving to the next version, review:

* Documentation clarity
* Safety alignment
* Scope boundary
* Data model consistency
* Terminology consistency
* Abuse potential
* Contribution readiness
* GitHub readability
* Missing examples
* Missing templates

---

## Current Status

Current target version:

```text
v0.1 Community Draft
```

Current priority:

```text
documentation consistency
local verification
smoke testing
backend coverage
frontend workflow polish
future safe validation workflow design
```
