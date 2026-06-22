# Data Model

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This document defines the initial data model for RedOps Framework.

The data model describes core entities, relationships, status values, required fields, and future implementation notes.

The model supports project scope, assets, ATT&CK mapping, campaigns, actions, evidence, findings, reports, telemetry, approvals, audit logs, and LLM-assisted workflow.

---

## Scope

The data model covers:

* User and role model
* Project model
* Scope model
* Asset model
* ATT&CK registry model
* Campaign model
* Action log model
* Evidence model
* Finding model
* Report model
* Telemetry model
* Approval model
* Audit log model
* LLM assistance model

This document is implementation-neutral. Future implementation may use SQL, document storage, or hybrid storage.

The current backend implementation uses SQLAlchemy models in `backend/app/models`
with JSON fields for structured metadata and list-like fields. Some sections
below keep future entities for product planning; implemented fields are mirrored
in `frontend/src/types/index.ts`.

---

## Entity List

Core entities:

```text
users
roles
user_roles
projects
project_members
scopes
assets
attack_collections
attack_tactics
attack_techniques
attack_relationships
campaigns
campaign_steps
actions
evidence
findings
finding_evidence
reports
telemetry
detection_gaps
approvals
audit_logs
llm_tasks
```

Optional future entities:

```text
organizations
workspaces
api_tokens
integrations
import_jobs
report_templates
external_tool_results
validation_workflows
validation_results
```

---

## Primary Relationships

```text
users -> project_members
roles -> user_roles
projects -> project_members
projects -> scopes
projects -> assets
projects -> campaigns
projects -> actions
projects -> evidence
projects -> findings
projects -> reports
projects -> telemetry
projects -> audit_logs

campaigns -> campaign_steps
campaign_steps -> attack_techniques
campaign_steps -> assets
campaign_steps -> actions
campaign_steps -> telemetry

actions -> evidence
actions -> telemetry
findings -> evidence
findings -> assets
findings -> attack_techniques
findings -> telemetry
reports -> findings
reports -> evidence
telemetry -> evidence
approvals -> campaign_steps
audit_logs -> users
```

---

## User Model

The user model stores account identity.

Fields:

```text
user_id
email
full_name
password_hash
is_active
created_at
updated_at
last_login_at
```

Required fields:

```text
user_id
email
full_name
is_active
created_at
```

Example:

```yaml
user:
  user_id: user-001
  email: operator@example.com
  full_name: Operator Example
  is_active: true
```

---

## Role Model

The role model stores system role names.

Initial roles:

```text
admin
lead_operator
operator
reviewer
client_viewer
```

Fields:

```text
role_id
name
description
created_at
updated_at
```

Example:

```yaml
role:
  role_id: role-001
  name: lead_operator
  description: Can create projects, define scope, plan campaigns, and review reports.
```

---

## User Role Model

The user role model maps users to roles.

Fields:

```text
user_role_id
user_id
role_id
created_at
```

Rules:

1. A user may have multiple roles.
2. Role changes must be logged.
3. Admin role assignment should require review in production implementation.

---

## Project Model

The project model stores engagement-level data.

Fields:

```text
project_id
name
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

Engagement type values:

```text
external_pentest
internal_pentest
web_application_pentest
mobile_application_pentest
cloud_security_assessment
red_team
assumed_breach
purple_team
internal_assessment
```

Example:

```yaml
project:
  project_id: project-001
  name: Example Red Team Assessment
  client_name: Example Client
  engagement_type: red_team
  status: draft
  start_date: 2026-06-20
  end_date: 2026-06-30
```

---

## Project Member Model

The project member model maps users to projects.

Fields:

```text
project_member_id
project_id
user_id
project_role
created_at
```

Project role values:

```text
lead_operator
operator
reviewer
client_viewer
```

Rules:

1. A user must be a project member to access project data.
2. Project member changes must be logged.
3. Client viewer access should be limited to finalized report output.

---

## Scope Model

The scope model stores approved project boundaries.

Fields:

```text
scope_id
project_id
allowed_targets
forbidden_targets
test_window
rules_of_engagement
restricted_actions
approval_required
emergency_contact
status
notes
created_by
reviewed_by
created_at
updated_at
```

Scope status values:

```text
draft
pending_review
approved
expired
revoked
```

Example:

```yaml
scope:
  scope_id: scope-001
  project_id: project-001
  allowed_targets:
    - type: domain
      value: app.example.com
    - type: ip_range
      value: 10.10.10.0/24
  forbidden_targets:
    - type: domain
      value: payment.example.com
  approval_required: true
  status: approved
```

Rules:

1. A project must have approved scope before campaign planning.
2. Scope changes must be logged.
3. Expired or revoked scope must block new campaign steps.
4. Forbidden targets must not be selectable.

---

## Asset Model

The asset model stores project assets.

Fields:

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

Asset type values:

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

Environment values:

```text
production
staging
development
lab
unknown
```

Criticality values:

```text
low
medium
high
critical
unknown
```

Example:

```yaml
asset:
  asset_id: asset-001
  project_id: project-001
  asset_type: application
  asset_value: customer-portal-staging
  environment: staging
  criticality: high
  tags:
    - web
    - external
```

---

## ATT&CK Collection Model

The ATT&CK collection model stores dataset metadata.

Fields:

```text
collection_id
domain
name
description
content_version
source
created_at_source
modified_at_source
imported_at
```

Domain values:

```text
enterprise
mobile
ics
```

---

## ATT&CK Tactic Model

The ATT&CK tactic model stores tactics.

Fields:

```text
tactic_id
attack_id
short_name
name
description
domain
content_version
created_at_source
modified_at_source
```

Example:

```yaml
attack_tactic:
  attack_id: TA0007
  short_name: discovery
  name: Discovery
  domain: enterprise
```

---

## ATT&CK Technique Model

The ATT&CK technique model stores techniques and sub-techniques.

Fields:

```text
technique_id
attack_id
name
description
domain
tactics
platforms
data_components
detection
mitigations
references
is_subtechnique
parent_attack_id
content_version
created_at_source
modified_at_source
revoked
deprecated
raw_stix
```

Required fields:

```text
attack_id
name
domain
content_version
revoked
deprecated
```

Example:

```yaml
attack_technique:
  attack_id: T1057
  name: Process Discovery
  domain: enterprise
  tactics:
    - discovery
  platforms:
    - Windows
    - Linux
    - macOS
  is_subtechnique: false
  revoked: false
  deprecated: false
```

---

## ATT&CK Relationship Model

The ATT&CK relationship model stores relationships between ATT&CK objects.

Fields:

```text
relationship_id
source_ref
target_ref
relationship_type
description
domain
content_version
created_at_source
modified_at_source
raw_stix
```

Relationship type examples:

```text
uses
mitigates
detects
subtechnique-of
revoked-by
related-to
```

---

## Campaign Model

The campaign model stores project campaign plans.

Fields:

```text
campaign_id
project_id
name
objective
assumption
status
created_by
approved_by
started_at
completed_at
created_at
updated_at
```

Campaign status values:

```text
draft
planned
approved
active
completed
cancelled
```

Example:

```yaml
campaign:
  campaign_id: campaign-001
  project_id: project-001
  name: Endpoint Discovery Visibility Review
  objective: Review endpoint visibility for discovery behavior.
  status: draft
```

---

## Campaign Step Model

The campaign step model stores planned campaign steps.

Fields:

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
approval_id
status
executed_by
executed_at
created_at
updated_at
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

Example:

```yaml
campaign_step:
  campaign_step_id: step-001
  campaign_id: campaign-001
  step_order: 1
  attack_technique_id: T1057
  target_asset_id: asset-001
  objective: Review endpoint process discovery visibility.
  approval_required: true
  status: planned
```

Rules:

1. A campaign step must belong to a campaign.
2. A campaign step should reference an ATT&CK technique when applicable.
3. A campaign step should reference a target asset.
4. Restricted steps require approval.
5. Step changes must be logged.

---

## Action Model

The action model stores operator activity and validation results.

Fields:

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

Action type values:

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

Action result values:

```text
unknown
planned
approved
executed
skipped
failed
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

Example:

```yaml
action:
  action_id: action-001
  project_id: project-001
  campaign_step_id: step-001
  asset_id: asset-001
  operator_id: user-001
  action_type: detection_validation_note
  action_summary: Reviewed endpoint telemetry for discovery activity.
  detection_status: partially_detected
```

---

## Evidence Model

The evidence model stores evidence metadata.

Fields:

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
sanitized
captured_at
uploaded_at
created_at
updated_at
```

Evidence type values:

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
manual_note
other
```

Example:

```yaml
evidence:
  evidence_id: evidence-001
  project_id: project-001
  action_id: action-001
  asset_id: asset-001
  uploaded_by: user-001
  evidence_type: edr_alert
  file_name: endpoint-event-review.txt
  file_hash_sha256: example-hash
```

Rules:

1. Evidence must belong to a project.
2. Evidence should link to an action or finding when applicable.
3. Uploaded files must store SHA256 hash.
4. Evidence download must be logged.
5. Evidence examples in the repository must be sanitized.

---

## Finding Model

The finding model stores project findings.

Fields:

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

Example:

```yaml
finding:
  finding_id: finding-001
  project_id: project-001
  title: Endpoint discovery activity was partially detected
  severity: medium
  affected_assets:
    - asset-001
  attack_technique_id: T1057
  status: draft
```

---

## Finding Evidence Model

The finding evidence model links findings and evidence.

Fields:

```text
finding_evidence_id
finding_id
evidence_id
relationship_note
created_at
```

Rules:

1. A finding may have multiple evidence records.
2. Evidence may support multiple findings.
3. Evidence relationship should be reviewed before final report generation.

---

## Report Model

The report model stores report metadata and generated output references.

Fields:

```text
report_id
project_id
title
version
status
format
file_path
generated_by
generated_at
created_at
updated_at
```

Report status values:

```text
draft
generated
under_review
approved
final
archived
```

Report format values:

```text
markdown
html
pdf
docx_later
```

Example:

```yaml
report:
  report_id: report-001
  project_id: project-001
  title: Example Red Team Assessment Report
  version: "0.1"
  status: draft
  format: markdown
```

---

## Telemetry Model

The telemetry model stores expected and observed telemetry.

Fields:

```text
telemetry_id
project_id
campaign_id
campaign_step_id
action_id
finding_id
asset_id
evidence_id
attack_technique_id
expected_telemetry
observed_telemetry
data_source
detection_status
review_note
reviewed_by
reviewed_at
created_at
updated_at
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

Example:

```yaml
telemetry:
  telemetry_id: telemetry-001
  project_id: project-001
  campaign_step_id: step-001
  action_id: action-001
  asset_id: asset-001
  evidence_id: evidence-001
  attack_technique_id: T1057
  expected_telemetry:
    - name: process_creation
      data_source: edr
      data_component: Process Creation
      signal: Process discovery activity should create endpoint process telemetry.
      required: true
  observed_telemetry:
    - name: process_creation
      data_source: edr
      data_component: Process Creation
      signal: Sanitized endpoint event linked to evidence.
      required: false
  detection_status: partially_detected
```

---

## Detection Gap Model

The detection gap model stores missing or incomplete telemetry records.

Fields:

```text
gap_id
project_id
telemetry_id
campaign_step_id
finding_id
evidence_id
asset_id
attack_technique_id
gap_type
summary
impact
recommendation
status
created_by
created_at
updated_at
```

Detection gap type values:

```text
missing_telemetry
incomplete_telemetry
delayed_telemetry
low_confidence_signal
missing_data_source
missing_detection_rule
blocked_before_detection
not_reviewed
```

Example:

```yaml
detection_gap:
  gap_id: gap-001
  project_id: project-001
  telemetry_id: telemetry-001
  campaign_step_id: step-001
  evidence_id: evidence-001
  asset_id: asset-001
  attack_technique_id: T1057
  gap_type: incomplete_telemetry
  summary: Process creation was observed, but command execution context was unavailable.
  status: open
```

---

## Approval Model

The approval model stores approval records.

Fields:

```text
approval_id
project_id
entity_type
entity_id
requested_by
decided_by
status
risk_level
reason
conditions
decision_note
requested_at
decided_at
expires_at
created_at
updated_at
```

Approval status values:

```text
pending
approved
rejected
expired
revoked
```

Risk level values:

```text
standard
controlled
sensitive
high_risk
```

Entity type values:

```text
campaign
action_type
scope
policy_exception
```

Rules:

1. Approval must reference a project.
2. Approval must reference an entity.
3. Approval must expire when used for restricted action.
4. Revoked approval must block related workflow.
5. Approval changes must be logged.

---

## Audit Log Model

The audit log model stores important project activity.

Fields:

```text
audit_log_id
project_id
actor_user_id
action
resource_type
resource_id
summary
detail
created_at
```

Audit event examples:

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
llm_output_accepted
```

Rules:

1. Audit logs should be append-only.
2. Audit logs must include actor identity when available.
3. Audit logs must include timestamp.
4. Audit logs must not store credentials or secrets.
5. Sensitive changes should store safe summaries instead of raw sensitive values.

---

## LLM Task Model

The LLM task model stores metadata for LLM-assisted work.

Fields:

```text
llm_task_id
project_id
task_type
entity_type
entity_id
requested_by
input_summary
output_content
assumptions
limitations
status
reviewed_by
reviewed_at
created_at
updated_at
```

Task type values:

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

Status values:

```text
under_review
accepted
rejected
archived
```

Rules:

1. LLM task output must be reviewed before acceptance.
2. Accepted LLM output must create an audit event.
3. Sensitive prompts and raw outputs should not be stored when they contain restricted data.
4. Output hash may be stored for traceability.

---

## Future Validation Workflow Model

The validation workflow model may be added in future versions.

Fields:

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
created_by
created_at
updated_at
```

Workflow status values:

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

The validation workflow model should be added only after the safety model and approval model are stable.

---

## Implementation Notes

Suggested database:

```text
PostgreSQL
```

Suggested ID format:

```text
UUID
```

Suggested structured fields:

```text
JSONB
```

Suggested timestamp format:

```text
UTC ISO 8601
```

Suggested file hash:

```text
SHA256
```

Suggested implementation stack:

```text
FastAPI
SQLAlchemy
Alembic
PostgreSQL
```

---

## JSONB Candidate Fields

Fields that may use JSONB in PostgreSQL:

```text
allowed_targets
forbidden_targets
rules_of_engagement
restricted_actions
tags
tactics
platforms
data_components
mitigations
references
raw_stix
expected_telemetry
observed_telemetry
conditions
old_value
new_value
affected_assets
```

---

## Index Candidates

Suggested indexes:

```text
users.email
projects.status
projects.engagement_type
project_members.project_id
project_members.user_id
assets.project_id
assets.asset_type
assets.asset_value
attack_techniques.attack_id
attack_techniques.domain
attack_techniques.content_version
campaigns.project_id
campaign_steps.campaign_id
campaign_steps.attack_technique_id
actions.project_id
actions.campaign_step_id
evidence.project_id
evidence.action_id
evidence.finding_id
findings.project_id
findings.severity
findings.status
telemetry.project_id
telemetry.detection_status
approvals.project_id
approvals.entity_type
audit_logs.project_id
audit_logs.actor_user_id
audit_logs.action
audit_logs.created_at
```

---

## Data Protection Notes

Sensitive data should not be stored unless required.

Avoid storing:

```text
credentials
tokens
private_keys
client_secrets
raw_sensitive_logs
personal_data
production_secrets
private_network_exports
```

When sensitive data is required:

1. Restrict access by project membership.
2. Mark the record as restricted.
3. Store only required fields.
4. Remove secrets from examples.
5. Log access to sensitive records.
6. Apply retention rules.

---

## Review Checklist

Use this checklist when reviewing data model changes.

```text
[ ] Entity has a clear purpose
[ ] Required fields are defined
[ ] Status values are defined
[ ] Relationships are defined
[ ] Sensitive fields are identified
[ ] Audit requirements are defined
[ ] Scope relationship is considered
[ ] Project relationship is considered
[ ] ATT&CK mapping is version-aware
[ ] LLM output requires review
[ ] Evidence integrity is preserved
[ ] Report usage is considered
```

---

## Current Status

Current version:

```text
v0.1 Community Draft
```

Current focus:

```text
core entities
entity relationships
status values
audit model
approval model
LLM task model
telemetry model
future validation workflow model
```
