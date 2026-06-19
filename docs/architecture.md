# Architecture

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This document describes the architecture of RedOps Framework.

The architecture covers the main system components, data flow, safety controls, LLM assistance, telemetry review, and future implementation layers.

The framework starts as a documentation-first model. Implementation should follow after the product scope, data model, safety model, and workflow are reviewed.

---

## Architecture Goals

The architecture supports the following goals:

* Manage authorized pentest and red team projects
* Define scope and target boundaries
* Store assets and project metadata
* Map objectives to MITRE ATT&CK
* Plan campaign steps
* Track operator actions
* Store evidence
* Manage findings
* Generate reports
* Record audit logs
* Support LLM-assisted planning and reporting
* Support future safe validation workflow
* Support future telemetry and detection feedback

---

## High-Level Model

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
  |-- Target allowlist
  |-- Restricted action policy
  |-- Approval workflow
  |-- Audit logging
  |
  v
Assistance and Validation Layer
  |
  |-- LLM assistance
  |-- Manual action record
  |-- External tool import
  |-- Safe validation workflow
  |-- Telemetry review
  |
  v
Project Output
  |
  |-- Evidence
  |-- Finding
  |-- ATT&CK mapping
  |-- Detection feedback
  |-- Report
```

---

## Component Overview

| Component         | Purpose                                                                          |
| ----------------- | -------------------------------------------------------------------------------- |
| Project Workspace | Stores project metadata, engagement type, status, members, and timeline          |
| Scope Manager     | Stores approved targets, forbidden targets, rules of engagement, and test window |
| Asset Registry    | Stores assets that belong to a project                                           |
| ATT&CK Registry   | Stores tactics, techniques, sub-techniques, relationships, and version metadata  |
| Campaign Planner  | Stores campaign objectives, planned steps, ATT&CK mapping, and approval status   |
| Action Log        | Stores operator actions, notes, result status, and detection status              |
| Evidence Vault    | Stores files and metadata used to support actions and findings                   |
| Finding Manager   | Stores findings, severity, impact, recommendation, and evidence links            |
| Report Builder    | Produces report output from project data                                         |
| Safety Gate       | Validates scope, approval, allowlist, policy, and audit requirements             |
| LLM Assistance    | Supports planning, review, evidence summary, finding draft, and report draft     |
| Telemetry Model   | Stores expected telemetry, observed telemetry, and detection status              |

---

## Core Data Flow

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
Import or reference ATT&CK data
  |
  v
Create campaign plan
  |
  v
Validate scope and policy
  |
  v
Record action or validation result
  |
  v
Attach evidence
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

## Project Workspace

The Project Workspace is the root object for engagement data.

It stores:

```text
project_id
project_name
client_name
engagement_type
description
status
start_date
end_date
created_by
created_at
updated_at
```

Project status values:

```text
draft
active
paused
completed
archived
```

A project links to:

```text
scope
assets
campaigns
actions
evidence
findings
reports
audit_logs
members
```

---

## Scope Manager

Scope Manager defines the project boundary.

It stores:

```text
allowed_targets
forbidden_targets
test_window
rules_of_engagement
restricted_actions
approval_required
emergency_contact
notes
```

Scope Manager is used by:

```text
Campaign Planner
Safety Gate
Action Log
Evidence Vault
Finding Manager
Report Builder
LLM Assistance
```

Scope validation is required before workflow-related artifacts are accepted.

---

## Asset Registry

Asset Registry stores target references and metadata.

Asset types:

```text
ip_address
ip_range
domain
subdomain
url
cloud_account
repository
wireless_network
application
api
identity_tenant
lab_environment
```

Asset fields:

```text
asset_id
project_id
asset_type
asset_value
environment
owner
criticality
tags
notes
created_at
updated_at
```

Assets are used by:

```text
campaign steps
action logs
evidence
findings
reports
scope validation
```

---

## ATT&CK Registry

ATT&CK Registry stores ATT&CK content in a local model.

Registry entities:

```text
attack_tactic
attack_technique
attack_subtechnique
attack_relationship
attack_data_component
attack_mitigation
attack_reference
```

Technique fields:

```text
attack_id
name
description
tactic
platforms
data_components
detection
mitigations
references
is_subtechnique
parent_technique_id
content_version
created_at_source
modified_at_source
revoked
deprecated
```

Registry requirements:

1. Store ATT&CK content version.
2. Preserve deprecated and revoked status.
3. Support search by ATT&CK ID.
4. Support search by technique name.
5. Support filter by tactic.
6. Support filter by platform.
7. Support mapping to campaign steps.
8. Support mapping to findings.
9. Support mapping to telemetry expectations.

---

## Campaign Planner

Campaign Planner stores the operational plan for a project.

Campaign fields:

```text
campaign_id
project_id
campaign_name
objective
assumption
status
created_by
approved_by
started_at
completed_at
```

Campaign step fields:

```text
campaign_step_id
campaign_id
step_order
attack_technique_id
target_asset_id
objective
operator_note
expected_result
expected_telemetry
approval_required
status
executed_by
executed_at
```

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

## Action Log

Action Log records operator activity and workflow results.

Action fields:

```text
action_id
project_id
campaign_id
campaign_step_id
asset_id
operator_id
action_type
action_summary
action_detail
result
detection_status
started_at
ended_at
created_at
updated_at
```

Action types:

```text
manual_validation
configuration_review
recon_note
scanner_result
exploit_validation_note
access_validation_note
detection_validation_note
cleanup_note
```

Detection status values:

```text
unknown
detected
not_detected
blocked
partially_detected
not_applicable
```

---

## Evidence Vault

Evidence Vault stores files and metadata that support action records and findings.

Evidence types:

```text
screenshot
terminal_output
log_file
http_request_response
scanner_output
configuration_export
siem_alert
edr_alert
document
other
```

Evidence fields:

```text
evidence_id
project_id
action_id
finding_id
asset_id
uploaded_by
evidence_type
file_name
file_size
mime_type
file_hash_sha256
description
captured_at
uploaded_at
```

Evidence requirements:

1. Store file hash.
2. Store uploader identity.
3. Store upload time.
4. Link evidence to project.
5. Link evidence to action or finding when applicable.
6. Restrict evidence access by project membership.
7. Record evidence download in audit log.
8. Block sensitive data in public examples.

---

## Finding Manager

Finding Manager stores confirmed or draft findings.

Finding fields:

```text
finding_id
project_id
title
summary
severity
affected_assets
attack_technique_id
impact
likelihood
recommendation
status
created_by
reviewed_by
created_at
updated_at
```

Severity values:

```text
informational
low
medium
high
critical
```

Finding status values:

```text
draft
under_review
confirmed
risk_accepted
remediated
closed
```

Findings may link to:

```text
assets
evidence
actions
campaign_steps
attack_techniques
reports
```

---

## Report Builder

Report Builder creates structured report output from project data.

Report sections:

```text
Cover
Document Control
Executive Summary
Scope
Methodology
Engagement Timeline
Campaign Summary
Findings Summary
Technical Findings
ATT&CK Mapping
Detection Feedback
Remediation Plan
Evidence Appendix
Limitations
Cleanup Status
```

Output formats:

```text
markdown
html
pdf
docx_later
```

Report Builder reads from:

```text
project
scope
assets
campaigns
actions
evidence
findings
telemetry
audit_logs
```

---

## Safety Gate

Safety Gate validates workflow-related artifacts.

Safety Gate checks:

```text
project_status
scope_status
target_allowlist
forbidden_target
test_window
restricted_action
approval_status
role_permission
audit_requirement
cleanup_requirement
```

Safety Gate output:

```text
allowed
blocked
approval_required
requires_review
```

A blocked item should include:

```text
reason
policy_reference
required_fix
reviewer
timestamp
```

---

## LLM Assistance Layer

LLM Assistance Layer supports planning, analysis, and reporting.

LLM-supported tasks:

```text
scope_summary
attack_mapping_suggestion
campaign_plan_draft
policy_review
evidence_summary
finding_draft
remediation_draft
report_draft
telemetry_gap_analysis
cleanup_checklist
```

LLM output must pass:

```text
format_validation
schema_validation
attack_registry_validation
scope_validation
policy_validation
human_review
```

LLM output must not bypass:

```text
scope
approval
policy
role_permission
audit
```

---

## Telemetry Model

Telemetry Model stores expected and observed detection data.

Telemetry fields:

```text
telemetry_id
project_id
campaign_step_id
technique_id
expected_telemetry
observed_telemetry
data_source
detection_status
evidence_id
reviewed_by
reviewed_at
```

Detection status values:

```text
unknown
detected
not_detected
blocked
partially_detected
not_applicable
```

Telemetry Model is used by:

```text
Campaign Planner
Evidence Vault
Finding Manager
Report Builder
LLM Assistance
```

---

## External Tool Import

The architecture supports future import from external tools.

Import types:

```text
scanner_result
siem_alert
edr_alert
cloud_security_finding
burp_export
nuclei_result
openvas_result
nessus_result
manual_note
```

Import flow:

```text
Upload or import file
  |
  v
Parse content
  |
  v
Sanitize sensitive data
  |
  v
Map to project
  |
  v
Map to asset
  |
  v
Create evidence record
  |
  v
Create finding draft when applicable
  |
  v
Review
```

---

## Future Validation Layer

The future validation layer may support controlled validation workflows.

Validation layer components:

```text
workflow_definition
schema_validator
scope_validator
policy_validator
approval_checker
controlled_runner_interface
telemetry_collector
evidence_linker
cleanup_tracker
```

Validation workflow states:

```text
draft
pending_validation
pending_approval
approved
ready
executed
blocked
failed
cleanup_required
completed
cancelled
```

Execution-related work must remain scope-bound, approval-controlled, and audit-logged.

---

## Logical Architecture

```text
+-------------------------------------------------------+
|                    User Interface                     |
|-------------------------------------------------------|
| Dashboard | Projects | Campaigns | Evidence | Reports |
+---------------------------+---------------------------+
                            |
                            v
+-------------------------------------------------------+
|                     Backend API                       |
|-------------------------------------------------------|
| Auth | RBAC | Projects | Scope | Assets | Campaigns   |
| Actions | Evidence | Findings | Reports | Audit       |
+---------------------------+---------------------------+
                            |
                            v
+-------------------------------------------------------+
|                    Safety Gate                        |
|-------------------------------------------------------|
| Scope | Allowlist | Approval | Policy | Audit         |
+---------------------------+---------------------------+
                            |
                            v
+-------------------------------------------------------+
|                  Assistance Layer                     |
|-------------------------------------------------------|
| LLM Assistance | ATT&CK Mapping | Telemetry Review     |
+---------------------------+---------------------------+
                            |
                            v
+-------------------------------------------------------+
|                     Data Layer                        |
|-------------------------------------------------------|
| PostgreSQL | Object Storage | Search Index             |
+---------------------------+---------------------------+
                            |
                            v
+-------------------------------------------------------+
|                  External Sources                     |
|-------------------------------------------------------|
| ATT&CK STIX | Scanner Results | SIEM | EDR | Logs      |
+-------------------------------------------------------+
```

---

## Suggested Implementation Stack

| Layer         | Suggested Technology                                  |
| ------------- | ----------------------------------------------------- |
| Frontend      | React or Next.js                                      |
| Backend       | Python FastAPI                                        |
| Database      | PostgreSQL                                            |
| ORM           | SQLAlchemy                                            |
| Migration     | Alembic                                               |
| Auth          | JWT for MVP, SSO later                                |
| Storage       | Local filesystem for MVP, S3-compatible storage later |
| Queue         | Redis Queue or Celery later                           |
| Documentation | Markdown                                              |
| Diagrams      | Mermaid                                               |
| Schema        | JSON Schema                                           |

---

## API Boundary

Initial API groups:

```text
/auth
/users
/projects
/scopes
/assets
/attack
/campaigns
/actions
/evidence
/findings
/reports
/audit-logs
```

Future API groups:

```text
/llm
/policy
/telemetry
/imports
/validation-workflows
```

---

## Storage Boundary

Data storage types:

| Data Type                  | Storage                         |
| -------------------------- | ------------------------------- |
| Project metadata           | PostgreSQL                      |
| Scope records              | PostgreSQL                      |
| Asset records              | PostgreSQL                      |
| ATT&CK registry            | PostgreSQL                      |
| Campaign records           | PostgreSQL                      |
| Action logs                | PostgreSQL                      |
| Evidence metadata          | PostgreSQL                      |
| Evidence files             | Local storage or object storage |
| Finding records            | PostgreSQL                      |
| Report metadata            | PostgreSQL                      |
| Report files               | Local storage or object storage |
| Audit logs                 | PostgreSQL                      |
| Diagrams and documentation | Git repository                  |

---

## Security Boundary

Security controls:

```text
authentication
role_based_access
project_membership_check
scope_validation
allowlist_validation
approval_workflow
audit_logging
evidence_access_control
file_integrity_hashing
sensitive_data_sanitization
```

Security-sensitive operations:

```text
scope_update
approval_change
evidence_download
finding_review
report_generation
restricted_action_approval
validation_workflow_acceptance
llm_output_acceptance
```

---

## Deployment Model

Initial deployment model:

```text
single workspace
single database
local storage
manual user management
documentation-first repository
```

Future deployment model:

```text
multi-project workspace
object storage
background worker
external tool import
SSO
audit export
report export
LLM provider configuration
```

---

## Architecture Review Checklist

Use this checklist before implementation work:

```text
[ ] Project model is defined
[ ] Scope model is defined
[ ] Asset model is defined
[ ] ATT&CK registry model is defined
[ ] Campaign model is defined
[ ] Action log model is defined
[ ] Evidence model is defined
[ ] Finding model is defined
[ ] Report model is defined
[ ] Audit model is defined
[ ] Safety Gate behavior is defined
[ ] LLM Assistance boundary is defined
[ ] Telemetry Model is defined
[ ] Repository structure is stable
[ ] Roadmap is aligned with architecture
```

---

## Current Status

Current version:

```text
v0.1 Community Draft
```

Current focus:

```text
workspace architecture
scope and policy control
LLM assistance boundary
evidence and finding workflow
report output
future validation layer
```
