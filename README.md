# RedOps Framework

An ATT&CK-based framework for managing authorized pentest and red team operations.

![Status](https://img.shields.io/badge/status-community%20draft-blue)
![Version](https://img.shields.io/badge/version-0.1-blue)
![License](https://img.shields.io/badge/license-Apache--2.0-green)

---

## Overview

RedOps Framework defines a structured model for managing pentest and red team operations.

It covers project scope, asset inventory, ATT&CK mapping, campaign planning, action tracking, evidence handling, finding management, reporting, audit trail, safety control, and LLM-assisted workflow.

The framework is intended for authorized security assessment, internal security validation, red team planning, purple team activity, and security consulting delivery.

---

## What It Does

RedOps Framework helps teams manage security operations through a consistent workflow.

Core functions:

* Define project scope and rules of engagement
* Register target assets and metadata
* Map objectives to MITRE ATT&CK tactics and techniques
* Build campaign plans
* Track operator actions
* Store evidence with metadata
* Link findings to assets, evidence, actions, and ATT&CK techniques
* Generate technical and executive reports
* Record audit logs
* Support LLM-assisted planning, analysis, and reporting

---

## Use Cases

| Use Case             | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| Pentest engagement   | Manage scope, assets, findings, evidence, and reporting      |
| Red team operation   | Plan and track campaigns using ATT&CK techniques             |
| Purple team exercise | Compare expected telemetry with observed detection results   |
| Detection validation | Record detection status for controlled validation steps      |
| Security consulting  | Produce structured report output from engagement data        |
| Internal assessment  | Maintain repeatable workflow for authorized internal testing |

---

## Core Components

| Component         | Purpose                                                                           |
| ----------------- | --------------------------------------------------------------------------------- |
| Project Workspace | Stores engagement-level information                                               |
| Scope Manager     | Defines allowed targets, restricted actions, and test window                      |
| Asset Registry    | Stores systems, applications, cloud accounts, domains, APIs, and related metadata |
| ATT&CK Registry   | Stores ATT&CK tactics, techniques, sub-techniques, data sources, and references   |
| Campaign Planner  | Maps operation objectives to ATT&CK techniques and planned steps                  |
| Action Log        | Records operator activity and execution notes                                     |
| Evidence Vault    | Stores screenshots, logs, command output, scanner output, and other evidence      |
| Finding Manager   | Tracks findings, affected assets, severity, impact, and recommendation            |
| Report Builder    | Generates report output from project data                                         |
| Safety Gate       | Enforces scope, approval, allowlist, and restricted action policy                 |
| Telemetry Model   | Maps expected and observed telemetry to detection status                          |
| LLM Assistance    | Supports planning, review, evidence summary, finding draft, and report draft      |

---

## Architecture

```text
User
  |
  v
RedOps Workspace
  |
  |-- Project Workspace
  |-- Scope Manager
  |-- Asset Registry
  |-- ATT&CK Registry
  |-- Campaign Planner
  |-- Action Log
  |-- Evidence Vault
  |-- Finding Manager
  |-- Report Builder
  |
  v
Safety Gate
  |
  |-- Scope validation
  |-- Approval check
  |-- Target allowlist
  |-- Restricted action policy
  |-- Audit logging
  |
  v
Validation Layer
  |
  |-- Manual action record
  |-- Safe validation workflow
  |-- External tool import
  |-- Telemetry review
  |
  v
Output
  |
  |-- Evidence
  |-- Finding
  |-- ATT&CK mapping
  |-- Detection feedback
  |-- Report
```

---

## LLM Assistance

LLM support is used for planning, review, analysis, and documentation.

Supported areas:

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

Execution remains controlled by project scope, policy validation, approval workflow, and audit logging.

Recommended flow:

```text
User request
  |
  v
LLM plan draft
  |
  v
Schema validation
  |
  v
ATT&CK registry validation
  |
  v
Scope and policy validation
  |
  v
Human approval
  |
  v
Controlled validation workflow
  |
  v
Telemetry and evidence review
  |
  v
Finding and report output
```

---

## Safety Model

The framework uses the following safety controls:

* Authorized scope is required before campaign planning
* Target allowlist is required for operation tracking
* Restricted actions require approval
* Forbidden actions are blocked by policy
* Evidence access is limited by project membership
* Important changes are recorded in audit logs
* High-risk validation workflows require additional review
* Production execution requires explicit authorization
* Lab and controlled environments are preferred for validation workflows

Policy categories:

| Category                       | Default Handling                         |
| ------------------------------ | ---------------------------------------- |
| Documentation                  | Allowed                                  |
| Manual validation record       | Allowed                                  |
| Scanner result import          | Allowed                                  |
| Safe validation workflow       | Approval required                        |
| Exploit validation             | Approval required and scope-bound        |
| Credential exposure validation | Lab account or temporary credential only |
| Persistence validation         | Reversible and cleanup-required          |
| Destructive action             | Forbidden                                |

---

## Data Model

Initial data entities:

```text
users
roles
projects
project_members
scopes
assets
attack_tactics
attack_techniques
campaigns
campaign_steps
actions
evidence
findings
reports
approvals
audit_logs
```

Primary relationships:

```text
project -> scopes
project -> assets
project -> campaigns
project -> findings
project -> reports

campaign -> campaign_steps
campaign_step -> attack_technique
campaign_step -> action

action -> evidence
finding -> evidence
finding -> attack_technique
finding -> asset
```

---

## Repository Structure

```text
redops-framework/
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── .gitignore
│
├── docs/
│   ├── overview.md
│   ├── product-scope.md
│   ├── architecture.md
│   ├── attack-registry.md
│   ├── llm-assistance.md
│   ├── safety-model.md
│   ├── telemetry-model.md
│   ├── data-model.md
│   ├── api.md
│   ├── roadmap.md
│   └── glossary.md
│
├── schemas/
│   ├── project.schema.json
│   ├── scope.schema.json
│   ├── asset.schema.json
│   ├── campaign.schema.json
│   ├── action.schema.json
│   ├── evidence.schema.json
│   ├── finding.schema.json
│   └── report.schema.json
│
├── examples/
│   ├── project.example.yaml
│   ├── scope.example.yaml
│   ├── campaign.example.yaml
│   ├── finding.example.md
│   └── report-outline.example.md
│
├── templates/
│   ├── finding-template.md
│   ├── report-template.md
│   ├── campaign-plan-template.md
│   └── rules-of-engagement-template.md
│
├── diagrams/
│   ├── architecture-overview.mmd
│   ├── workflow-overview.mmd
│   └── llm-assisted-flow.mmd
│
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── documentation.yml
    │   ├── feature_request.yml
    │   └── security_model.yml
    └── PULL_REQUEST_TEMPLATE.md
```

---

## Documentation

Detailed documents are stored in `docs/`.

| Document                  | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| `docs/overview.md`        | Project overview and operating model       |
| `docs/product-scope.md`   | Product modules and workflow scope         |
| `docs/architecture.md`    | System architecture and component model    |
| `docs/attack-registry.md` | ATT&CK data import and registry model      |
| `docs/llm-assistance.md`  | LLM-assisted workflow model                |
| `docs/safety-model.md`    | Scope, approval, policy, and audit control |
| `docs/telemetry-model.md` | Detection feedback and telemetry mapping   |
| `docs/data-model.md`      | Data entities and relationships            |
| `docs/api.md`             | API structure proposal                     |
| `docs/roadmap.md`         | Development roadmap                        |
| `docs/glossary.md`        | Project terminology                        |

---

## Roadmap

### v0.1

* Community README
* Repository structure
* Product scope draft
* Safety model draft
* LLM assistance draft
* Roadmap draft

### v0.2

* ATT&CK registry model
* STIX import design
* Data model draft
* JSON schema draft
* Example project files

### v0.3

* Campaign planning model
* Action log model
* Evidence model
* Finding model
* Report template

### v0.4

* Policy gate design
* Approval workflow
* Audit trail design
* Role and permission model

### v0.5

* LLM-assisted planning workflow
* LLM-assisted evidence review
* LLM-assisted finding and report draft
* Prompt boundary and validation policy

### v0.6

* Safe validation workflow model
* Controlled runner interface
* External tool import design

### v0.7

* Telemetry model
* Detection feedback workflow
* Expected and observed telemetry mapping
* Report section for detection feedback

### v1.0

* Stable framework specification
* Complete documentation set
* Example workflows
* Contribution process
* Security policy

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/<owner>/redops-framework.git
cd redops-framework
```

Review the main documents:

```text
README.md
docs/overview.md
docs/safety-model.md
docs/llm-assistance.md
docs/roadmap.md
```

Start with the templates:

```text
templates/rules-of-engagement-template.md
templates/campaign-plan-template.md
templates/finding-template.md
templates/report-template.md
```

Review example files:

```text
examples/project.example.yaml
examples/scope.example.yaml
examples/campaign.example.yaml
examples/finding.example.md
examples/report-outline.example.md
```

---

## Security Policy

This project is intended for authorized security work.

Accepted use:

* Internal security assessment
* Approved pentest engagement
* Approved red team engagement
* Purple team exercise
* Detection engineering
* Lab-based validation
* Security control review

Rejected use:

* Unauthorized access
* Unauthorized scanning
* Credential theft
* Malware deployment
* Evasion tooling
* Persistence deployment on unauthorized systems
* Destructive operations
* Activity outside approved scope

For security concerns related to this project, contact:

```text
Kenshin Himura
roxlab.org@gmail.com
```

---

## Contributing

Contributions are welcome in the following areas:

* Documentation
* Data model
* JSON schema
* Example workflow
* Report template
* Safety model
* LLM assistance model
* ATT&CK registry design
* Telemetry model
* API proposal

Contribution rules:

* Keep all examples within authorized security use
* Avoid destructive workflow examples
* Avoid evasion content
* Avoid credential theft content
* Avoid payload delivery content
* Document assumptions and limitations
* Use clear technical language
* Keep changes reviewable

See `CONTRIBUTING.md` for details.

---

## Author

Kenshin Himura
[roxlab.org@gmail.com](mailto:roxlab.org@gmail.com)

---

## License

Apache-2.0

See `LICENSE` for details.
