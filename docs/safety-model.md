# Safety Model

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This document defines the safety model for RedOps Framework.

The safety model describes how the framework handles scope, approval, policy, audit, evidence integrity, LLM-assisted workflow, and controlled validation.

The goal is to keep all project activity bound to authorized security work.

---

## Safety Principles

RedOps Framework uses the following principles:

* Authorized use only
* Scope-bound workflow
* Target allowlist
* Approval-based sensitive actions
* Role-based access
* Audit logging
* Evidence integrity
* Human review for LLM-generated output
* Reversible validation workflow
* Lab-first validation for higher-risk workflows

---

## Authorized Use

Accepted use cases:

* Internal security assessment
* Approved pentest engagement
* Approved red team engagement
* Purple team exercise
* Detection engineering
* Security control validation
* Lab-based validation
* Security consulting workflow
* Evidence and finding management
* Report generation

Every project must have defined scope and approval before execution-related workflow is tracked.

---

## Prohibited Use

The framework must not be used for:

* Unauthorized access
* Unauthorized scanning
* Unauthorized exploitation
* Credential theft
* Malware deployment
* Payload delivery
* Evasion tooling
* Destructive operations
* Activity outside approved scope
* Activity against systems without written authorization
* Persistence deployment on unauthorized systems
* Any activity that violates law, policy, contract, or rules of engagement

---

## Scope Model

Scope defines the operational boundary of a project.

Minimum scope fields:

```text
project_id
allowed_targets
forbidden_targets
test_window
rules_of_engagement
restricted_actions
approval_required
emergency_contact
notes
```

Target types:

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

Scope status values:

```text
draft
pending_review
approved
expired
revoked
```

---

## Scope Rules

Required rules:

1. A project must have approved scope before campaign planning.
2. Campaign steps must reference targets inside the approved scope.
3. Forbidden targets must not be selectable.
4. Restricted actions must require approval.
5. Scope changes must be logged.
6. Scope expiration must block new campaign steps.
7. Revoked scope must block campaign execution and validation workflow.
8. Emergency contact must be visible to project members.
9. Rules of engagement must be linked to the project.
10. Scope must be included in the final report.

---

## Target Allowlist

The target allowlist defines assets that may be referenced by campaign steps, action logs, evidence, and findings.

Allowlist examples:

```yaml
allowed_targets:
  - type: domain
    value: example.com
  - type: subdomain
    value: app.example.com
  - type: ip_range
    value: 10.10.10.0/24
  - type: cloud_account
    value: aws-sandbox-001
  - type: application
    value: customer-portal-staging
```

Forbidden target examples:

```yaml
forbidden_targets:
  - type: domain
    value: production-payment.example.com
  - type: ip_range
    value: 10.20.0.0/16
  - type: cloud_account
    value: aws-production-main
```

Validation requirements:

* Exact match for domain, URL, repository, and application targets
* CIDR validation for IP range
* Environment tag validation for cloud account
* Project membership validation before access
* Audit log entry for allowlist changes

---

## Action Classification

Actions are classified by risk level.

| Level        | Description                                                                | Default Handling                  |
| ------------ | -------------------------------------------------------------------------- | --------------------------------- |
| `standard`   | Documentation, review, mapping, note-taking                                | Allowed                           |
| `controlled` | Safe validation workflow or scanner result import                          | Approval required                 |
| `sensitive`  | Exploit validation, credential exposure validation, persistence validation | Approval required and scope-bound |
| `high_risk`  | Workflow with increased operational impact                                 | Lead approval and lab preference  |
| `forbidden`  | Destructive, unauthorized, evasive, or out-of-scope activity               | Blocked                           |

---

## Restricted Action Policy

Restricted actions require explicit approval.

Restricted categories:

```text
safe_validation_workflow
exploit_validation
credential_exposure_validation
persistence_validation
lateral_movement_validation
egress_telemetry_validation
external_tool_execution
production_environment_validation
```

Restricted action requirements:

1. Approved project scope
2. Target allowlist match
3. Assigned operator
4. Approval record
5. Execution window check
6. Audit log entry
7. Evidence requirement
8. Cleanup requirement when state change is involved

---

## Forbidden Action Policy

Forbidden actions must be blocked.

Forbidden categories:

```text
unauthorized_access
unauthorized_scanning
credential_theft
malware_deployment
payload_delivery
evasion_tooling
destructive_operation
out_of_scope_activity
unapproved_persistence
unapproved_lateral_movement
unapproved_data_exfiltration
```

A forbidden action must not be converted into an executable workflow.

A forbidden action may be documented as a policy note, risk statement, or limitation when needed for reporting.

---

## Approval Workflow

Approval is required for controlled, sensitive, and high-risk actions.

Approval status values:

```text
not_required
pending
approved
rejected
expired
revoked
```

Approval record fields:

```text
approval_id
project_id
entity_type
entity_id
requested_by
approved_by
status
risk_level
reason
conditions
requested_at
approved_at
expires_at
```

Current implementation supports project-scoped approval requests for:

```text
campaign
action_type
scope
policy_exception
```

Restricted action categories from approved scope are enforced for matching
action log types. For example, `exploit_validation` requires an approved
`action_type` approval for `exploit_validation_note` before that action can be
recorded.

Approval rules:

1. The requester and approver should be different users when possible.
2. Approval must reference project scope.
3. Approval must define action boundary.
4. Approval must define target boundary.
5. Approval must expire.
6. Revoked approval must block related workflow.
7. Approval changes must be logged.

---

## Role-Based Access

Initial roles:

```text
admin
lead_operator
operator
reviewer
client_viewer
```

Access model:

| Capability                | Admin | Lead Operator | Operator | Reviewer | Client Viewer |
| ------------------------- | ----: | ------------: | -------: | -------: | ------------: |
| Manage users              |   Yes |            No |       No |       No |            No |
| Create project            |   Yes |           Yes |       No |       No |            No |
| Edit scope                |   Yes |           Yes |       No |       No |            No |
| Approve scope             |   Yes |           Yes |       No |       No |            No |
| Manage assets             |   Yes |           Yes |      Yes |       No |            No |
| Create campaign           |   Yes |           Yes |       No |       No |            No |
| Edit campaign step        |   Yes |           Yes |      Yes |       No |            No |
| Approve restricted action |   Yes |           Yes |       No |       No |            No |
| Create action log         |   Yes |           Yes |      Yes |       No |            No |
| Upload evidence           |   Yes |           Yes |      Yes |       No |            No |
| Create finding            |   Yes |           Yes |      Yes |       No |            No |
| Review finding            |   Yes |           Yes |       No |      Yes |            No |
| Generate report           |   Yes |           Yes |       No |      Yes |            No |
| View final report         |   Yes |           Yes |      Yes |      Yes |           Yes |
| View audit log            |   Yes |           Yes |       No |      Yes |            No |

---

## Audit Model

Audit logging is required for important project activity.

Required audit events:

```text
user_login
user_created
role_changed
project_created
project_updated
scope_created
scope_updated
scope_approved
scope_revoked
asset_created
asset_updated
campaign_created
campaign_updated
campaign_step_created
campaign_step_approved
action_log_created
evidence_uploaded
evidence_downloaded
finding_created
finding_updated
finding_reviewed
report_generated
approval_requested
approval_granted
approval_rejected
approval_revoked
```

Audit event fields:

```text
audit_id
actor_id
project_id
entity_type
entity_id
action
old_value
new_value
ip_address
user_agent
created_at
```

Audit requirements:

1. Audit logs must be append-only.
2. Audit logs must include actor identity.
3. Audit logs must include timestamp.
4. Audit logs must include target entity.
5. Sensitive changes must include old and new values when safe to store.
6. Audit logs must not store credentials or secrets.
7. Audit logs must be available for review.

---

## Evidence Integrity

Evidence must be stored with metadata and integrity checks.

Required evidence fields:

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

Evidence rules:

1. Every uploaded file must have a SHA256 hash.
2. File names must be sanitized.
3. MIME type must be validated.
4. File size limit must be enforced.
5. Evidence access must follow project membership.
6. Evidence download must be logged.
7. Evidence must not contain credentials or secrets.
8. Evidence containing sensitive data must be marked as restricted.
9. Real client data must not be committed to the repository.
10. Example evidence must be sanitized.

---

## LLM-Assisted Safety

LLM assistance is allowed for planning, review, analysis, and documentation.

Allowed LLM tasks:

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

Restricted LLM tasks:

```text
direct_execution
scope_expansion
approval_bypass
payload_generation
credential_theft
evasion_instruction
malware_generation
destructive_action
out_of_scope_planning
```

LLM output validation requirements:

1. Schema validation
2. ATT&CK registry validation
3. Scope validation
4. Policy validation
5. Human approval for controlled or sensitive actions
6. Audit log entry for accepted plan changes

LLM output must not be treated as authorization.

---

## Validation Workflow Safety

Safe validation workflows must be controlled and reviewable.

Required workflow fields:

```text
workflow_id
project_id
mode
scope_ref
target_ref
technique_ref
risk_level
approval_ref
expected_telemetry
cleanup_required
revert_required
status
```

Allowed workflow status values:

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

Validation workflow requirements:

1. Workflow must reference approved scope.
2. Workflow must reference allowed target.
3. Workflow must define expected telemetry.
4. Workflow must define cleanup requirement.
5. Workflow must define revert requirement when state change is involved.
6. Workflow must not run when approval is missing.
7. Workflow result must be linked to evidence.
8. Workflow result must be logged.

---

## Cleanup and Revert

Cleanup is required when a validation workflow creates temporary state.

Cleanup fields:

```text
cleanup_required
cleanup_steps
cleanup_owner
cleanup_due_at
cleanup_status
cleanup_evidence
```

Cleanup status values:

```text
not_required
pending
completed
failed
requires_review
```

Revert is required when a workflow changes system state.

Revert status values:

```text
not_required
pending
completed
failed
requires_review
```

Rules:

1. Cleanup status must be tracked.
2. Failed cleanup must create a review item.
3. Revert failure must block workflow completion.
4. Cleanup evidence should be attached when available.
5. Cleanup and revert actions must be logged.

---

## Telemetry Review

Validation should be reviewed through expected and observed telemetry.

Telemetry status values:

```text
unknown
detected
not_detected
blocked
partially_detected
not_applicable
```

Telemetry fields:

```text
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

Telemetry rules:

1. Expected telemetry should be defined before validation.
2. Observed telemetry should be linked to evidence.
3. Detection status should be recorded.
4. Missing telemetry should be documented.
5. Detection gap should be included in reports when relevant.

---

## External Tool Import

The framework may import results from external tools.

Allowed import types:

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

Import rules:

1. Imported data must be linked to a project.
2. Imported data must be linked to an asset when possible.
3. Imported data must be reviewed before becoming a finding.
4. Imported data must not contain secrets.
5. Imported data must be sanitized before public sharing.
6. Import activity must be logged.

---

## Safety Checklist

Use this checklist before approving controlled or sensitive workflow:

```text
[ ] Project scope is approved
[ ] Target is in allowlist
[ ] Target is not in forbidden list
[ ] Test window is valid
[ ] Rules of engagement are attached
[ ] Emergency contact is available
[ ] Operator is assigned
[ ] Action classification is correct
[ ] Approval is recorded
[ ] Expected telemetry is defined
[ ] Evidence requirement is defined
[ ] Cleanup requirement is defined
[ ] Revert requirement is defined when needed
[ ] LLM-generated content has been reviewed
[ ] Audit logging is enabled
```

---

## Report Requirements

Reports should include safety-relevant context:

* Project scope
* Test window
* Rules of engagement summary
* Approved targets
* Excluded targets
* Campaign summary
* Findings
* Evidence references
* ATT&CK mapping
* Detection feedback
* Limitations
* Cleanup status

Reports should not include secrets, credentials, private keys, or sensitive raw logs unless approved and protected.

---

## Review Requirements

The safety model should be reviewed when:

* A new module is added
* A new workflow type is proposed
* A new external tool integration is proposed
* LLM-assisted workflow is changed
* Scope validation is changed
* Approval behavior is changed
* Audit requirements are changed
* Evidence handling is changed

---

## Current Status

Current version:

```text
v0.1 Community Draft
```

Current focus:

```text
scope
approval
audit
evidence integrity
LLM-assisted safety
controlled validation workflow
```
