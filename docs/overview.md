# Overview

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

RedOps Framework defines a structured model for managing authorized pentest and red team operations.

The framework covers project scope, asset inventory, ATT&CK mapping, campaign planning, action tracking, evidence handling, finding management, reporting, audit trail, safety controls, telemetry review, and LLM-assisted workflow.

This document provides a high-level overview of the framework and explains how the main components work together.

---

## Intended Audience

This framework is intended for:

* Pentesters
* Red team operators
* Purple team operators
* Security consultants
* Security engineers
* Detection engineers
* SOC analysts
* Internal security teams
* Security program owners

---

## Intended Use

Accepted use cases:

* Authorized pentest engagement
* Authorized red team engagement
* Internal security assessment
* Purple team exercise
* Detection validation
* Security control review
* Campaign planning
* Evidence management
* Finding management
* Report generation
* LLM-assisted documentation and review

All activity must be performed inside approved scope and rules of engagement.

---

## Project Scope

RedOps Framework is documentation-first, with the product model and safety
boundaries leading implementation.

The current repository includes the core documentation set plus an implemented
backend API and frontend console for the primary workflow. The scope remains:

* Product model
* Component model
* Safety model
* LLM assistance model
* Data model
* ATT&CK registry model
* Telemetry model
* API implementation reference
* Example files
* Templates
* Roadmap

Implementation work should continue to follow the reviewed core model.

---

## Framework Summary

RedOps Framework organizes security operations into the following flow:

```text
Project
  |
  v
Scope
  |
  v
Assets
  |
  v
ATT&CK Mapping
  |
  v
Campaign Plan
  |
  v
Action Log
  |
  v
Evidence
  |
  v
Finding
  |
  v
Report
```

Each step creates a project artifact that can be reviewed, linked, and audited.

---

## Main Concepts

| Concept          | Description                                                                   |
| ---------------- | ----------------------------------------------------------------------------- |
| Project          | Engagement-level workspace                                                    |
| Scope            | Approved target boundary and rules of engagement                              |
| Asset            | Target system, application, cloud account, API, repository, or related object |
| ATT&CK Technique | Tactic or technique reference from MITRE ATT&CK                               |
| Campaign         | Planned operation linked to project objectives                                |
| Campaign Step    | Individual planned step mapped to an asset and ATT&CK technique               |
| Action           | Operator record or validation result                                          |
| Evidence         | File or record that supports an action or finding                             |
| Finding          | Security issue or detection gap identified during the project                 |
| Report           | Structured output generated from project data                                 |
| Audit Log        | Record of important project activity                                          |
| Safety Gate      | Policy layer that validates scope, approval, and restricted actions           |
| LLM Assistance   | Support layer for planning, analysis, and documentation                       |

---

## Core Components

### Project Workspace

Stores project metadata, engagement type, members, timeline, and status.

### Scope Manager

Stores allowed targets, forbidden targets, test window, rules of engagement, restricted actions, approval requirements, and emergency contact.

### Asset Registry

Stores project assets and metadata such as environment, owner, criticality, tags, and notes.

### ATT&CK Registry

Stores ATT&CK tactics, techniques, sub-techniques, references, and version metadata.

### Campaign Planner

Stores campaign objectives, planned steps, target assets, ATT&CK mapping, expected results, expected telemetry, and approval status.

### Action Log

Stores operator activity, action summary, result, detection status, and timestamps.

### Evidence Vault

Stores evidence files and metadata, including file hash, type, uploader, asset reference, action reference, and finding reference.

### Finding Manager

Stores findings, severity, affected assets, impact, likelihood, recommendation, evidence links, and review status.

### Report Builder

Creates report output from project data, findings, evidence, ATT&CK mapping, detection feedback, and limitations.

### Safety Gate

Validates project scope, target allowlist, restricted action policy, approval status, role permission, and audit requirements.

### LLM Assistance

Supports scope summary, ATT&CK mapping suggestion, campaign plan draft, evidence summary, finding draft, remediation draft, report draft, telemetry gap analysis, and cleanup checklist.

### Telemetry Model

Stores expected telemetry, observed telemetry, detection status, evidence reference, and review notes.

---

## Operating Workflow

A typical project workflow:

```text
1. Create project
2. Define scope
3. Register assets
4. Import or reference ATT&CK data
5. Create campaign plan
6. Review scope and policy
7. Approve restricted actions when required
8. Record actions
9. Upload evidence
10. Create findings
11. Review findings
12. Generate report
13. Archive project
```

---

## Project Lifecycle

Project status values:

```text
draft
active
paused
completed
archived
```

### Draft

The project has been created but is not ready for active work.

### Active

The project has approved scope and can be used for campaign planning and project activity.

### Paused

The project is temporarily stopped.

### Completed

The engagement work has been completed and report output can be finalized.

### Archived

The project is retained for reference.

---

## Campaign Lifecycle

Campaign status values:

```text
draft
pending_approval
approved
in_progress
completed
cancelled
```

Campaign step status values:

```text
planned
pending_approval
approved
executed
skipped
blocked
failed
detected
not_detected
requires_review
```

---

## Finding Lifecycle

Finding status values:

```text
draft
under_review
confirmed
risk_accepted
remediated
closed
```

Finding severity values:

```text
informational
low
medium
high
critical
```

A finding should include:

* Title
* Summary
* Severity
* Affected assets
* ATT&CK mapping, when applicable
* Evidence references
* Impact
* Likelihood
* Recommendation
* Review status

---

## Safety Model Summary

The framework uses the following controls:

* Approved scope
* Target allowlist
* Forbidden target list
* Test window
* Restricted action policy
* Approval workflow
* Role-based access
* Audit logging
* Evidence integrity
* LLM output review
* Cleanup and revert tracking for controlled validation workflow

See `docs/safety-model.md` for details.

---

## LLM Assistance Summary

LLM assistance can support:

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

LLM-generated output must be reviewed and validated before it becomes a project artifact.

Validation requirements:

```text
format validation
schema validation
ATT&CK registry validation
scope validation
policy validation
human review
```

See `docs/llm-assistance.md` for details.

---

## ATT&CK Usage

MITRE ATT&CK is used as a reference model for tactics, techniques, sub-techniques, data components, mitigations, and references.

The framework uses ATT&CK for:

* Technique lookup
* Campaign mapping
* Finding mapping
* Detection feedback
* Coverage review
* Report output

ATT&CK data should be stored with version metadata to avoid unclear mappings when ATT&CK content changes.

See `docs/attack-registry.md` for details.

---

## Telemetry Review

Telemetry review compares expected detection signals with observed data.

Detection status values:

```text
unknown
detected
not_detected
blocked
partially_detected
not_applicable
```

Telemetry review can support:

* Detection validation
* Purple team activity
* Finding creation
* Report detection feedback
* Control coverage review

See `docs/telemetry-model.md` for details.

---

## Documentation Map

| File                      | Purpose                                |
| ------------------------- | -------------------------------------- |
| `README.md`               | Public project summary                 |
| `SECURITY.md`             | Security policy                        |
| `CONTRIBUTING.md`         | Contribution guidelines                |
| `docs/overview.md`        | High-level framework overview          |
| `docs/product-scope.md`   | Product scope and module boundaries    |
| `docs/architecture.md`    | System architecture                    |
| `docs/attack-registry.md` | ATT&CK registry model                  |
| `docs/llm-assistance.md`  | LLM assistance model                   |
| `docs/safety-model.md`    | Safety model                           |
| `docs/telemetry-model.md` | Telemetry and detection feedback model |
| `docs/data-model.md`      | Data entities and relationships        |
| `docs/api.md`             | API structure and implementation notes |
| `docs/smoke-test-checklist.md` | Manual end-to-end verification checklist |
| `docs/roadmap.md`         | Project roadmap                        |
| `docs/glossary.md`        | Terminology                            |

---

## Repository Layout

```text
redops-framework/
├── README.md
├── SECURITY.md
├── CONTRIBUTING.md
├── docs/
├── schemas/
├── examples/
├── templates/
├── diagrams/
└── .github/
```

Folder usage:

| Folder       | Purpose                                                     |
| ------------ | ----------------------------------------------------------- |
| `docs/`      | Detailed framework documentation                            |
| `schemas/`   | JSON schema drafts                                          |
| `examples/`  | Example project, scope, campaign, finding, and report files |
| `templates/` | Reusable Markdown templates                                 |
| `diagrams/`  | Mermaid diagrams                                            |
| `.github/`   | GitHub issue and pull request templates                     |

---

## Current Version

Current version:

```text
v0.1 Community Draft
```

Current focus:

```text
documentation structure
security policy
contribution rules
roadmap
safety model
LLM assistance model
architecture
overview
```

---

## Next Documents

Recommended next documents:

```text
docs/product-scope.md
docs/attack-registry.md
docs/telemetry-model.md
docs/data-model.md
docs/api.md
docs/glossary.md
```
