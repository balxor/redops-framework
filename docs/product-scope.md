# Product Scope

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This document defines the product scope for RedOps Framework.

The product scope describes the modules, workflows, boundaries, user roles, and planned capability stages for the framework.

---

## Product Summary

RedOps Framework manages authorized pentest and red team operations.

The framework stores project scope, assets, ATT&CK mapping, campaign plans, actions, evidence, findings, reports, audit logs, safety rules, telemetry review, and LLM-assisted drafts.

The initial version is documentation-first. Implementation work should follow after the model is reviewed.

---

## Target Users

| User                | Description                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| Admin               | Manages users, roles, repository configuration, and global settings                                |
| Lead Operator       | Creates projects, defines scope, plans campaigns, approves restricted actions, and reviews reports |
| Operator            | Records actions, uploads evidence, creates findings, and updates campaign status                   |
| Reviewer            | Reviews findings, evidence, report content, and safety alignment                                   |
| Client Viewer       | Reviews finalized report output and approved project summaries                                     |
| Detection Engineer  | Reviews telemetry, detection status, and detection gaps                                            |
| Security Consultant | Uses the framework to structure delivery and documentation                                         |

---

## Primary Use Cases

| Use Case               | Scope                                                               |
| ---------------------- | ------------------------------------------------------------------- |
| Pentest engagement     | Manage scope, assets, findings, evidence, and report output         |
| Red team operation     | Plan and track campaign steps mapped to ATT&CK techniques           |
| Purple team exercise   | Compare planned activity with detection and telemetry results       |
| Detection validation   | Record expected telemetry, observed telemetry, and detection status |
| Security consulting    | Produce structured technical and executive deliverables             |
| Internal assessment    | Maintain repeatable security assessment workflow                    |
| LLM-assisted reporting | Draft summaries, findings, remediation text, and report sections    |

---

## Operating Modes

The same modules support two complementary ways of working. Modes are a framing
over shared data, not separate products — a project can use both.

### Pentest Mode

Focused on day-to-day assessment work: managing scope and targets, recording
findings with evidence, and producing reports.

| Emphasis        | Modules                                                        |
| --------------- | ------------------------------------------------------------- |
| Scope & targets | Scope Manager, Asset Registry                                 |
| Work & evidence | Action Log, Evidence Vault                                    |
| Outcomes        | Finding Manager, Report Builder                               |

### Red Team Mode

Focused on adversary emulation: planning an ATT&CK-mapped campaign, gating
sensitive steps behind approval, and reconciling activity against detection.

| Emphasis            | Modules                                                   |
| ------------------- | --------------------------------------------------------- |
| Attack path         | Campaign Planner (ATT&CK chain), ATT&CK Registry          |
| Control             | Safety Gate (manual approval for restricted steps)        |
| Detection feedback  | Telemetry Model, Action Log (detection status)            |
| Hygiene             | Cleanup tracking via Action Log + Audit Trail             |

Both modes share Project Workspace, Safety Gate, Audit Trail, LLM Assistance,
and the report pipeline.

---

## Product Modules

Initial modules:

```text
Project Workspace
Scope Manager
Asset Registry
ATT&CK Registry
Campaign Planner
Action Log
Evidence Vault
Finding Manager
Report Builder
Safety Gate
Telemetry Model
LLM Assistance
Audit Trail
```

---

## Module Scope

### Project Workspace

Project Workspace stores engagement-level information.

Included:

* Project metadata
* Client or business unit name
* Engagement type
* Project status
* Project members
* Timeline
* Linked scope
* Linked assets
* Linked campaigns
* Linked findings
* Linked reports

Excluded from early versions:

* Billing
* Contract management
* Time tracking
* Resource scheduling
* Client portal workflow beyond report viewing

---

### Scope Manager

Scope Manager stores the approved boundary of a project.

Included:

* Allowed targets
* Forbidden targets
* Test window
* Rules of engagement
* Restricted actions
* Approval requirement
* Emergency contact
* Scope status
* Scope change history

Excluded from early versions:

* Legal contract generation
* Automated authorization verification
* External ticketing integration
* Continuous target discovery

---

### Asset Registry

Asset Registry stores assets that belong to a project.

Included asset types:

* IP address
* IP range
* Domain
* Subdomain
* URL
* Cloud account
* Repository
* Wireless network
* Application
* API
* Identity tenant
* Lab environment

Included metadata:

* Environment
* Owner
* Criticality
* Tags
* Notes
* Scope relationship

Excluded from early versions:

* Continuous asset discovery
* CMDB synchronization
* Cloud inventory synchronization
* Network topology generation

---

### ATT&CK Registry

ATT&CK Registry stores ATT&CK tactics, techniques, sub-techniques, and related metadata.

Included:

* Tactics
* Techniques
* Sub-techniques
* Technique references
* Platforms
* Data components
* Mitigations
* Detection notes
* Content version
* Deprecated status
* Revoked status

Excluded from early versions:

* Automatic live ATT&CK sync
* Full graph query engine
* Threat actor profiling
* Procedure-level automation

---

### Campaign Planner

Campaign Planner stores project objectives and planned campaign steps.

Included:

* Campaign objective
* Assumptions
* ATT&CK technique mapping
* Target asset reference
* Step order
* Expected result
* Expected telemetry
* Approval requirement
* Step status
* Operator note

Excluded from early versions:

* Autonomous planning
* Automatic step execution
* Adaptive attack path generation
* Environment-specific exploit planning

---

### Action Log

Action Log records operator activity and validation results.

Included:

* Manual validation notes
* Configuration review notes
* Scanner result notes
* Access validation notes
* Detection validation notes
* Cleanup notes
* Result status
* Detection status
* Timestamp
* Operator identity
* Linked evidence

Excluded from early versions:

* Direct command execution
* Terminal session recording
* Automatic shell integration
* Autonomous action selection

---

### Evidence Vault

Evidence Vault stores evidence files and metadata.

Included evidence types:

* Screenshot
* Terminal output
* Log file
* HTTP request and response
* Scanner output
* Configuration export
* SIEM alert
* EDR alert
* Document
* Manual note

Included metadata:

* File name
* File size
* MIME type
* SHA256 hash
* Uploader
* Capture time
* Upload time
* Linked action
* Linked finding
* Linked asset

Excluded from early versions:

* Large-scale evidence deduplication
* Legal evidence chain management
* Encrypted evidence sharing portal
* Long-term retention automation

---

### Finding Manager

Finding Manager stores security findings and detection gaps.

Included:

* Title
* Summary
* Severity
* Affected assets
* ATT&CK mapping
* Evidence references
* Impact
* Likelihood
* Recommendation
* Status
* Reviewer note

Excluded from early versions:

* CVSS calculator
* SLA tracking
* Ticketing integration
* Automated vulnerability validation
* Remediation workflow automation

---

### Report Builder

Report Builder generates structured output from project data.

Included sections:

* Cover
* Document control
* Executive summary
* Scope
* Methodology
* Engagement timeline
* Campaign summary
* Findings summary
* Technical findings
* ATT&CK mapping
* Detection feedback
* Remediation plan
* Evidence appendix
* Limitations
* Cleanup status

Initial output formats:

```text
markdown
html
pdf
```

Future output format:

```text
docx
```

Excluded from early versions:

* Custom report designer
* Multi-language report generation
* Client-specific branding engine
* Automatic report approval routing

---

### Safety Gate

Safety Gate validates scope, target, approval, and policy requirements.

Included checks:

* Project status
* Scope status
* Target allowlist
* Forbidden target list
* Test window
* Restricted action policy
* Approval status
* Role permission
* Audit requirement
* Cleanup requirement

Excluded from early versions:

* External GRC integration
* Contract-aware policy engine
* Real-time enforcement on external tools
* Autonomous risk scoring

---

### Telemetry Model

Telemetry Model stores detection and observation results.

Included:

* Expected telemetry
* Observed telemetry
* Data source
* Detection status
* Evidence reference
* Reviewer
* Review timestamp
* Detection gap note

Detection status values:

```text
unknown
detected
not_detected
blocked
partially_detected
not_applicable
```

Excluded from early versions:

* Direct SIEM query execution
* Direct EDR query execution
* Detection rule deployment
* Detection engineering CI/CD

---

### LLM Assistance

LLM Assistance supports planning, review, analysis, and documentation.

Included:

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

Excluded:

* Direct execution
* Approval bypass
* Scope expansion without approval
* Payload generation
* Credential theft
* Evasion instruction
* Malware generation
* Destructive action
* Out-of-scope planning

---

### Audit Trail

Audit Trail stores important project activity.

Included events:

* User login
* User creation
* Role change
* Project creation
* Project update
* Scope creation
* Scope update
* Scope approval
* Asset creation
* Campaign creation
* Campaign step approval
* Action log creation
* Evidence upload
* Evidence download
* Finding update
* Finding review
* Report generation
* Approval request
* Approval decision
* LLM output acceptance

Excluded from early versions:

* Immutable external audit storage
* SIEM forwarding
* Compliance report automation
* Advanced anomaly detection

---

## Product Workflow

Main workflow:

```text
Create project
  |
  v
Define scope
  |
  v
Register assets
  |
  v
Map objective to ATT&CK
  |
  v
Create campaign plan
  |
  v
Validate scope and policy
  |
  v
Approve restricted steps
  |
  v
Record action
  |
  v
Upload evidence
  |
  v
Create finding
  |
  v
Review finding
  |
  v
Generate report
  |
  v
Archive project
```

---

## User Workflow by Role

### Admin

Admin workflow:

```text
Create users
Assign roles
Review system settings
Import ATT&CK data
Review audit logs
Manage repository-level configuration
```

### Lead Operator

Lead Operator workflow:

```text
Create project
Define scope
Register assets
Create campaign
Approve restricted steps
Review findings
Generate report
Close project
```

### Operator

Operator workflow:

```text
Review assigned project
Review scope
Record action
Upload evidence
Create finding draft
Update campaign step status
Add cleanup notes
```

### Reviewer

Reviewer workflow:

```text
Review evidence
Review finding
Check scope alignment
Check ATT&CK mapping
Check report content
Approve or return for revision
```

### Client Viewer

Client Viewer workflow:

```text
View final report
View approved summary
Review remediation plan
Review limitations
```

---

## Lifecycle Status Values

### Project Status

```text
draft
active
paused
completed
archived
```

### Scope Status

```text
draft
pending_review
approved
expired
revoked
```

### Campaign Status

```text
draft
pending_approval
approved
in_progress
completed
cancelled
```

### Campaign Step Status

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

### Finding Status

```text
draft
under_review
confirmed
risk_accepted
remediated
closed
```

### Approval Status

```text
not_required
pending
approved
rejected
expired
revoked
```

---

## MVP Scope

The first implementation-ready scope should include:

```text
Project Workspace
Scope Manager
Asset Registry
ATT&CK Registry
Campaign Planner
Action Log
Evidence Vault
Finding Manager
Report Builder
Safety Gate
Audit Trail
Basic LLM Assistance
```

MVP completion criteria:

1. A user can create a project.
2. A user can define project scope.
3. A user can register assets.
4. A user can reference ATT&CK techniques.
5. A user can create a campaign plan.
6. A user can record an action.
7. A user can upload evidence metadata.
8. A user can create a finding.
9. A user can generate a report outline.
10. Important changes are audit-logged.
11. Restricted steps require approval.
12. LLM-generated output requires review before acceptance.

---

## Early Out of Scope

The following capabilities are outside early versions:

```text
autonomous_exploitation
autonomous_lateral_movement
credential_dumping_automation
edr_or_av_bypass_automation
malware_generation
payload_delivery
phishing_delivery
destructive_testing
automatic_production_execution
direct_command_execution_by_llm
```

---

## Future Scope

Future versions may define:

```text
safe_validation_workflow
controlled_runner_interface
external_tool_import
siem_integration
edr_integration
scanner_import
burp_export_import
nuclei_result_import
object_storage_backend
multi_project_dashboard
multi_tenant_workspace
sso_integration
api_token_management
report_template_library
```

---

## Product Boundaries

### Included

The product includes:

* Workflow model
* Documentation model
* Data model
* Schema model
* Safety model
* LLM assistance boundary
* ATT&CK mapping model
* Evidence and finding model
* Report model
* Audit model

### Excluded

The product excludes:

* Unauthorized operation
* Autonomous offensive execution
* Payload delivery
* Malware functionality
* Evasion module
* Destructive workflow
* Credential theft workflow
* Execution without approval

---

## Documentation Deliverables

Product scope documentation should be supported by:

```text
README.md
AGENTS.md
docs/overview.md
docs/getting-started.md
docs/architecture.md
docs/safety-model.md
docs/llm-assistance.md
docs/attack-registry.md
docs/integrations.md
docs/telemetry-model.md
docs/data-model.md
docs/api.md
docs/roadmap.md
frontend/README.md
```

---

## Current Status

Current version:

```text
v0.1 Community Draft
```

Current focus:

```text
product module definition
workflow boundary
role workflow
MVP scope
future scope
out-of-scope boundary
```
