# API

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This document defines the initial API proposal for RedOps Framework.

The API supports project management, scope management, asset registry, ATT&CK registry, campaign planning, action logs, evidence, findings, reports, telemetry, approvals, audit logs, and LLM-assisted workflow.

This document is a design draft. It is not an implementation contract yet.

---

## API Goals

The API should support:

* Project creation and review
* Scope definition and approval
* Asset registration
* ATT&CK lookup and mapping
* Campaign planning
* Action log recording
* Evidence metadata management
* Finding management
* Report generation
* Telemetry review
* Approval workflow
* Audit log review
* LLM-assisted draft creation and review

---

## Base Path

Suggested base path:

```http
/api/v1
```

Example:

```http
GET /api/v1/projects
```

---

## Format

Default request and response format:

```text
application/json
```

File upload endpoints may use:

```text
multipart/form-data
```

---

## Authentication

Authentication endpoints:

```http
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
```

### Login Request

```json
{
  "email": "operator@example.com",
  "password": "example-password"
}
```

### Login Response

```json
{
  "access_token": "token",
  "refresh_token": "refresh-token",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Current User Response

```json
{
  "user_id": "user-001",
  "email": "operator@example.com",
  "full_name": "Operator Example",
  "roles": ["operator"],
  "is_active": true
}
```

---

## Authorization Model

Initial roles:

```text
admin
lead_operator
operator
reviewer
client_viewer
```

Authorization checks should include:

* User authentication
* Global role
* Project membership
* Project role
* Entity ownership when applicable
* Scope status
* Approval status
* Restricted action policy

---

## Common Response Fields

Most entities should include:

```text
id
created_at
updated_at
created_by
updated_by
```

Timestamps should use UTC ISO 8601 format.

Example:

```json
{
  "created_at": "2026-06-20T10:00:00Z",
  "updated_at": "2026-06-20T11:00:00Z"
}
```

---

## Pagination

List endpoints should support pagination.

Query parameters:

```http
?page=1&page_size=50
```

Response format:

```json
{
  "items": [],
  "page": 1,
  "page_size": 50,
  "total": 0
}
```

---

## Filtering

List endpoints should support filtering where relevant.

Example:

```http
GET /api/v1/projects?status=active&engagement_type=red_team
```

Example:

```http
GET /api/v1/findings?severity=high&status=confirmed
```

---

## Sorting

List endpoints may support sorting.

Example:

```http
GET /api/v1/findings?sort=severity&order=desc
```

Supported order values:

```text
asc
desc
```

---

## Error Format

Standard error response:

```json
{
  "error": {
    "code": "scope_validation_failed",
    "message": "Target is outside approved scope.",
    "details": {
      "target": "example.internal",
      "project_id": "project-001"
    }
  }
}
```

Common error codes:

```text
bad_request
unauthorized
forbidden
not_found
validation_error
scope_validation_failed
approval_required
approval_rejected
policy_blocked
conflict
rate_limited
internal_error
```

---

## HTTP Status Codes

| Status | Meaning                                 |
| ------ | --------------------------------------- |
| `200`  | Request succeeded                       |
| `201`  | Entity created                          |
| `202`  | Request accepted for processing         |
| `204`  | Request succeeded with no response body |
| `400`  | Invalid request                         |
| `401`  | Authentication required                 |
| `403`  | Permission denied                       |
| `404`  | Entity not found                        |
| `409`  | Conflict                                |
| `422`  | Validation failed                       |
| `429`  | Rate limit exceeded                     |
| `500`  | Server error                            |

---

## Users

### Endpoints

```http
GET    /api/v1/users
POST   /api/v1/users
GET    /api/v1/users/{user_id}
PATCH  /api/v1/users/{user_id}
DELETE /api/v1/users/{user_id}
```

### Create User Request

```json
{
  "email": "operator@example.com",
  "full_name": "Operator Example",
  "roles": ["operator"],
  "is_active": true
}
```

### User Response

```json
{
  "user_id": "user-001",
  "email": "operator@example.com",
  "full_name": "Operator Example",
  "roles": ["operator"],
  "is_active": true,
  "created_at": "2026-06-20T10:00:00Z"
}
```

---

## Projects

### Endpoints

```http
GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/projects/{project_id}
PATCH  /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}
```

### Create Project Request

```json
{
  "name": "Example Red Team Assessment",
  "client_name": "Example Client",
  "engagement_type": "red_team",
  "description": "Authorized red team assessment.",
  "start_date": "2026-06-20",
  "end_date": "2026-06-30"
}
```

### Project Response

```json
{
  "project_id": "project-001",
  "name": "Example Red Team Assessment",
  "client_name": "Example Client",
  "engagement_type": "red_team",
  "status": "draft",
  "start_date": "2026-06-20",
  "end_date": "2026-06-30",
  "created_by": "user-001",
  "created_at": "2026-06-20T10:00:00Z"
}
```

---

## Project Members

### Endpoints

```http
GET    /api/v1/projects/{project_id}/members
POST   /api/v1/projects/{project_id}/members
PATCH  /api/v1/projects/{project_id}/members/{member_id}
DELETE /api/v1/projects/{project_id}/members/{member_id}
```

### Add Member Request

```json
{
  "user_id": "user-002",
  "project_role": "operator"
}
```

---

## Scopes

### Endpoints

```http
GET    /api/v1/projects/{project_id}/scopes
POST   /api/v1/projects/{project_id}/scopes
GET    /api/v1/scopes/{scope_id}
PATCH  /api/v1/scopes/{scope_id}
POST   /api/v1/scopes/{scope_id}/submit-review
POST   /api/v1/scopes/{scope_id}/approve
POST   /api/v1/scopes/{scope_id}/revoke
```

### Create Scope Request

```json
{
  "allowed_targets": [
    {
      "type": "domain",
      "value": "app.example.com"
    },
    {
      "type": "ip_range",
      "value": "10.10.10.0/24"
    }
  ],
  "forbidden_targets": [
    {
      "type": "domain",
      "value": "payment.example.com"
    }
  ],
  "test_window": {
    "start": "2026-06-20T22:00:00Z",
    "end": "2026-06-21T02:00:00Z"
  },
  "rules_of_engagement": "Approved testing only during the test window.",
  "restricted_actions": [
    "exploit_validation",
    "persistence_validation"
  ],
  "approval_required": true,
  "emergency_contact": {
    "name": "Security Contact",
    "email": "security@example.com"
  }
}
```

### Scope Response

```json
{
  "scope_id": "scope-001",
  "project_id": "project-001",
  "status": "draft",
  "allowed_targets": [],
  "forbidden_targets": [],
  "approval_required": true,
  "created_at": "2026-06-20T10:00:00Z"
}
```

---

## Assets

### Endpoints

```http
GET    /api/v1/projects/{project_id}/assets
POST   /api/v1/projects/{project_id}/assets
GET    /api/v1/assets/{asset_id}
PATCH  /api/v1/assets/{asset_id}
DELETE /api/v1/assets/{asset_id}
```

### Create Asset Request

```json
{
  "asset_type": "application",
  "asset_value": "customer-portal-staging",
  "environment": "staging",
  "owner": "application-team",
  "criticality": "high",
  "tags": ["web", "external"],
  "notes": "Authorized test target."
}
```

### Asset Response

```json
{
  "asset_id": "asset-001",
  "project_id": "project-001",
  "asset_type": "application",
  "asset_value": "customer-portal-staging",
  "environment": "staging",
  "criticality": "high",
  "created_at": "2026-06-20T10:00:00Z"
}
```

---

## ATT&CK Registry

### Endpoints

```http
POST /api/v1/attack/import
GET  /api/v1/attack/imports
GET  /api/v1/attack/imports/{import_id}
GET  /api/v1/attack/collections
GET  /api/v1/attack/tactics
GET  /api/v1/attack/techniques
GET  /api/v1/attack/techniques/{technique_id}
GET  /api/v1/attack/search
```

### Search Examples

```http
GET /api/v1/attack/search?q=process discovery
GET /api/v1/attack/techniques?attack_id=T1057
GET /api/v1/attack/techniques?tactic=discovery
GET /api/v1/attack/techniques?platform=Windows
GET /api/v1/attack/techniques?domain=enterprise
```

### Technique Response

```json
{
  "technique_id": "technique-001",
  "attack_id": "T1057",
  "name": "Process Discovery",
  "domain": "enterprise",
  "tactics": ["discovery"],
  "platforms": ["Windows", "Linux", "macOS"],
  "is_subtechnique": false,
  "parent_attack_id": null,
  "content_version": "unknown",
  "revoked": false,
  "deprecated": false
}
```

---

## Campaigns

### Endpoints

```http
GET    /api/v1/projects/{project_id}/campaigns
POST   /api/v1/projects/{project_id}/campaigns
GET    /api/v1/campaigns/{campaign_id}
PATCH  /api/v1/campaigns/{campaign_id}
DELETE /api/v1/campaigns/{campaign_id}
POST   /api/v1/campaigns/{campaign_id}/submit-review
POST   /api/v1/campaigns/{campaign_id}/approve
POST   /api/v1/campaigns/{campaign_id}/cancel
```

### Create Campaign Request

```json
{
  "name": "Endpoint Discovery Visibility Review",
  "objective": "Review endpoint visibility for discovery behavior.",
  "assumption": "Endpoint telemetry is available for reviewed assets."
}
```

### Campaign Response

```json
{
  "campaign_id": "campaign-001",
  "project_id": "project-001",
  "name": "Endpoint Discovery Visibility Review",
  "objective": "Review endpoint visibility for discovery behavior.",
  "status": "draft",
  "created_by": "user-001",
  "created_at": "2026-06-20T10:00:00Z"
}
```

---

## Campaign Steps

### Endpoints

```http
GET    /api/v1/campaigns/{campaign_id}/steps
POST   /api/v1/campaigns/{campaign_id}/steps
GET    /api/v1/campaign-steps/{step_id}
PATCH  /api/v1/campaign-steps/{step_id}
DELETE /api/v1/campaign-steps/{step_id}
POST   /api/v1/campaign-steps/{step_id}/approve
POST   /api/v1/campaign-steps/{step_id}/mark-executed
POST   /api/v1/campaign-steps/{step_id}/mark-skipped
POST   /api/v1/campaign-steps/{step_id}/mark-blocked
```

### Create Campaign Step Request

```json
{
  "step_order": 1,
  "attack_technique_id": "T1057",
  "target_asset_id": "asset-001",
  "objective": "Review endpoint process discovery visibility.",
  "expected_result": "Relevant endpoint telemetry is available for review.",
  "expected_telemetry": [
    "process_creation",
    "command_execution"
  ],
  "approval_required": true
}
```

### Campaign Step Response

```json
{
  "campaign_step_id": "step-001",
  "campaign_id": "campaign-001",
  "step_order": 1,
  "attack_technique_id": "T1057",
  "target_asset_id": "asset-001",
  "status": "planned",
  "approval_required": true
}
```

---

## ATT&CK Mapping

### Endpoints

```http
POST /api/v1/campaign-steps/{step_id}/attack-mapping
POST /api/v1/findings/{finding_id}/attack-mapping
POST /api/v1/telemetry/{telemetry_id}/attack-mapping
```

### Create Mapping Request

```json
{
  "attack_id": "T1057",
  "domain": "enterprise",
  "content_version": "unknown",
  "mapping_note": "Mapped to endpoint discovery visibility review.",
  "requires_review": true
}
```

---

## Actions

### Endpoints

```http
GET   /api/v1/projects/{project_id}/actions
POST  /api/v1/projects/{project_id}/actions
GET   /api/v1/actions/{action_id}
PATCH /api/v1/actions/{action_id}
```

### Create Action Request

```json
{
  "campaign_id": "campaign-001",
  "campaign_step_id": "step-001",
  "asset_id": "asset-001",
  "action_type": "detection_validation_note",
  "action_summary": "Reviewed endpoint telemetry for the campaign step.",
  "action_detail": "Telemetry was reviewed from the approved data source.",
  "result": "Partial telemetry was available.",
  "detection_status": "partially_detected"
}
```

### Action Response

```json
{
  "action_id": "action-001",
  "project_id": "project-001",
  "campaign_step_id": "step-001",
  "action_type": "detection_validation_note",
  "detection_status": "partially_detected",
  "created_at": "2026-06-20T10:00:00Z"
}
```

---

## Evidence

### Endpoints

```http
GET    /api/v1/projects/{project_id}/evidence
POST   /api/v1/projects/{project_id}/evidence
POST   /api/v1/projects/{project_id}/evidence/upload
GET    /api/v1/evidence/{evidence_id}
PATCH  /api/v1/evidence/{evidence_id}
DELETE /api/v1/evidence/{evidence_id}
GET    /api/v1/evidence/{evidence_id}/download
```

### Create Evidence Metadata Request

```json
{
  "action_id": "action-001",
  "finding_id": null,
  "asset_id": "asset-001",
  "evidence_type": "edr_alert",
  "file_name": "endpoint-event-review.txt",
  "file_size": 2048,
  "mime_type": "text/plain",
  "file_hash_sha256": "example-hash",
  "description": "Sanitized endpoint telemetry review note.",
  "captured_at": "2026-06-20T10:30:00Z"
}
```

### Evidence Response

```json
{
  "evidence_id": "evidence-001",
  "project_id": "project-001",
  "action_id": "action-001",
  "asset_id": "asset-001",
  "evidence_type": "edr_alert",
  "file_name": "endpoint-event-review.txt",
  "file_hash_sha256": "example-hash",
  "uploaded_by": "user-001",
  "uploaded_at": "2026-06-20T10:35:00Z"
}
```

---

## Findings

### Endpoints

```http
GET    /api/v1/projects/{project_id}/findings
POST   /api/v1/projects/{project_id}/findings
GET    /api/v1/findings/{finding_id}
PATCH  /api/v1/findings/{finding_id}
DELETE /api/v1/findings/{finding_id}
POST   /api/v1/findings/{finding_id}/review
POST   /api/v1/findings/{finding_id}/confirm
POST   /api/v1/findings/{finding_id}/close
```

### Create Finding Request

```json
{
  "title": "Endpoint discovery activity was partially detected",
  "summary": "Telemetry review found partial coverage for the reviewed campaign step.",
  "severity": "medium",
  "affected_assets": ["asset-001"],
  "attack_technique_id": "T1057",
  "impact": "Investigation context may be incomplete.",
  "likelihood": "Medium",
  "recommendation": "Review endpoint logging policy, EDR configuration, and SIEM parsing."
}
```

### Finding Response

```json
{
  "finding_id": "finding-001",
  "project_id": "project-001",
  "title": "Endpoint discovery activity was partially detected",
  "severity": "medium",
  "status": "draft",
  "attack_technique_id": "T1057",
  "created_at": "2026-06-20T10:00:00Z"
}
```

---

## Finding Evidence

### Endpoints

```http
GET    /api/v1/findings/{finding_id}/evidence
POST   /api/v1/findings/{finding_id}/evidence
DELETE /api/v1/findings/{finding_id}/evidence/{evidence_id}
```

### Link Evidence Request

```json
{
  "evidence_id": "evidence-001",
  "relationship_note": "Supports telemetry review for the finding."
}
```

---

## Reports

### Endpoints

```http
GET  /api/v1/projects/{project_id}/reports
POST /api/v1/projects/{project_id}/reports
POST /api/v1/projects/{project_id}/reports/generate
GET  /api/v1/reports/{report_id}
GET  /api/v1/reports/{report_id}/download
PATCH /api/v1/reports/{report_id}
```

### Generate Report Request

```json
{
  "title": "Example Red Team Assessment Report",
  "format": "markdown",
  "include_sections": [
    "executive_summary",
    "scope",
    "campaign_summary",
    "findings_summary",
    "technical_findings",
    "attack_mapping",
    "detection_feedback",
    "remediation_plan",
    "limitations"
  ]
}
```

The current implementation generates a deterministic outline from recorded
project data. It does not call an LLM or execute external tooling.

### Report Response

```json
{
  "report_id": "report-001",
  "project_id": "project-001",
  "title": "Example Red Team Assessment Report",
  "version": "0.1",
  "format": "markdown",
  "status": "generated",
  "generated_by": "user-001",
  "generated_at": "2026-06-20T10:00:00Z"
}
```

---

## Telemetry

### Endpoints

```http
GET    /api/v1/projects/{project_id}/telemetry
POST   /api/v1/projects/{project_id}/telemetry
PATCH  /api/v1/projects/{project_id}/telemetry/{telemetry_id}
```

### Create Telemetry Record Request

```json
{
  "campaign_step_id": "step-001",
  "finding_id": null,
  "asset_id": "asset-001",
  "evidence_id": "evidence-001",
  "attack_technique_id": "T1057",
  "expected_telemetry": [
    {
      "name": "process_creation",
      "data_source": "edr",
      "data_component": "Process Creation",
      "signal": "Process discovery activity should create endpoint process telemetry.",
      "required": true
    }
  ],
  "observed_telemetry": [
    {
      "name": "process_creation",
      "data_source": "edr",
      "data_component": "Process Creation",
      "signal": "Sanitized endpoint event linked to evidence.",
      "required": false
    }
  ],
  "data_source": "edr",
  "detection_status": "partially_detected",
  "review_note": "Command execution context was not available in the reviewed evidence."
}
```

### Telemetry Response

```json
{
  "telemetry_id": "telemetry-001",
  "project_id": "project-001",
  "campaign_step_id": "step-001",
  "asset_id": "asset-001",
  "evidence_id": "evidence-001",
  "attack_technique_id": "T1057",
  "detection_status": "partially_detected",
  "reviewed_at": "2026-06-20T10:00:00Z"
}
```

---

## Detection Gaps

### Endpoints

```http
GET    /api/v1/projects/{project_id}/detection-gaps
POST   /api/v1/projects/{project_id}/detection-gaps
PATCH  /api/v1/projects/{project_id}/detection-gaps/{gap_id}
```

### Create Detection Gap Request

```json
{
  "telemetry_id": "telemetry-001",
  "campaign_step_id": "step-001",
  "finding_id": "finding-001",
  "evidence_id": "evidence-001",
  "asset_id": "asset-001",
  "attack_technique_id": "T1057",
  "gap_type": "incomplete_telemetry",
  "summary": "Process creation was observed, but command execution context was unavailable.",
  "impact": "Investigation context may be incomplete.",
  "recommendation": "Review endpoint logging policy, EDR configuration, and SIEM parsing.",
  "status": "open"
}
```

---

## Approvals

### Endpoints

```http
GET  /api/v1/projects/{project_id}/approvals
POST /api/v1/projects/{project_id}/approvals
POST /api/v1/projects/{project_id}/approvals/{approval_id}/approve
POST /api/v1/projects/{project_id}/approvals/{approval_id}/reject
POST /api/v1/projects/{project_id}/approvals/{approval_id}/revoke
```

### Create Approval Request

```json
{
  "entity_type": "action_type",
  "entity_id": "exploit_validation_note",
  "risk_level": "controlled",
  "reason": "Approval required for controlled validation workflow.",
  "conditions": {
    "scope_required": true,
    "evidence_required": true,
    "cleanup_required": false
  },
  "expires_at": "2026-06-21T00:00:00Z"
}
```

### Approval Response

```json
{
  "approval_id": "approval-001",
  "project_id": "project-001",
  "entity_type": "action_type",
  "entity_id": "exploit_validation_note",
  "risk_level": "controlled",
  "status": "pending",
  "requested_by": "user-001",
  "requested_at": "2026-06-20T10:00:00Z"
}
```

---

## Audit Logs

### Endpoints

```http
GET /api/v1/projects/{project_id}/audit
```

### Audit Log Response

```json
{
  "audit_log_id": "audit-001",
  "project_id": "project-001",
  "actor_user_id": "user-001",
  "action": "scope.created",
  "resource_type": "scope",
  "resource_id": "scope-001",
  "summary": "Scope created with status approved",
  "detail": {},
  "created_at": "2026-06-20T10:00:00Z"
}
```

---

## LLM Assistance

### Endpoints

```http
POST /api/v1/projects/{project_id}/llm/tasks
GET  /api/v1/projects/{project_id}/llm/tasks
POST /api/v1/projects/{project_id}/llm/tasks/{llm_task_id}/accept
POST /api/v1/projects/{project_id}/llm/tasks/{llm_task_id}/reject
```

### Create LLM Task Request

```json
{
  "task_type": "campaign_plan_draft",
  "entity_type": "campaign",
  "entity_id": "campaign-001",
  "input_summary": "Draft a campaign plan from approved scope and sanitized objective.",
  "output_content": "Structured draft content requiring human review.",
  "assumptions": ["Scope is approved"],
  "limitations": ["Draft only; not authorization"],
  "requires_review": true
}
```

### LLM Task Response

```json
{
  "llm_task_id": "llm-task-001",
  "project_id": "project-001",
  "task_type": "campaign_plan_draft",
  "status": "under_review",
  "requires_review": true,
  "created_at": "2026-06-20T10:00:00Z"
}
```

### LLM Review Request

```json
{
  "review_note": "Accepted as campaign draft after scope review."
}
```

Rules:

1. LLM-generated output must be reviewed before acceptance.
2. Accepted LLM output must create an audit event.
3. LLM output must not bypass scope, approval, or policy.
4. Sensitive raw prompts and outputs should not be stored when restricted data is present.

---

## Imports

### Endpoints

```http
GET  /api/v1/projects/{project_id}/imports
POST /api/v1/projects/{project_id}/imports
GET  /api/v1/imports/{import_id}
```

Supported import types:

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
attack_stix
```

### Create Import Request

```json
{
  "import_type": "scanner_result",
  "source_name": "example-scanner",
  "description": "Sanitized scanner output import."
}
```

---

## Future Validation Workflows

Future endpoints may be defined for safe validation workflows.

Draft endpoints:

```http
GET  /api/v1/projects/{project_id}/validation-workflows
POST /api/v1/projects/{project_id}/validation-workflows
GET  /api/v1/validation-workflows/{workflow_id}
PATCH /api/v1/validation-workflows/{workflow_id}
POST /api/v1/validation-workflows/{workflow_id}/validate
POST /api/v1/validation-workflows/{workflow_id}/approve
POST /api/v1/validation-workflows/{workflow_id}/record-result
POST /api/v1/validation-workflows/{workflow_id}/record-cleanup
```

Rules:

1. Workflow must reference approved scope.
2. Workflow must reference allowed target.
3. Workflow must define expected telemetry.
4. Workflow must define approval requirement.
5. Workflow result must be linked to evidence.
6. Workflow activity must be logged.

Execution behavior is outside the early API scope.

---

## Safety Gate API

Safety Gate may expose validation endpoints.

Draft endpoints:

```http
POST /api/v1/policy/validate-scope
POST /api/v1/policy/validate-target
POST /api/v1/policy/validate-action
POST /api/v1/policy/validate-llm-output
POST /api/v1/policy/validate-campaign-step
```

### Policy Validation Request

```json
{
  "project_id": "project-001",
  "entity_type": "campaign_step",
  "entity_id": "step-001",
  "target_asset_id": "asset-001",
  "action_type": "detection_validation_note"
}
```

### Policy Validation Response

```json
{
  "result": "approval_required",
  "reasons": [
    "Campaign step requires approval."
  ],
  "required_actions": [
    "request_approval"
  ]
}
```

Result values:

```text
allowed
blocked
approval_required
requires_review
```

---

## Rate Limiting

Suggested default:

```text
100 requests per minute per user
```

Higher-risk endpoints may use lower limits:

```text
approval endpoints
import endpoints
file upload endpoints
LLM endpoints
future validation workflow endpoints
```

---

## Audit Requirements by Endpoint Group

| Endpoint Group | Audit Required                         |
| -------------- | -------------------------------------- |
| Auth           | Login and logout events                |
| Users          | Create, update, role change            |
| Projects       | Create, update, archive                |
| Scopes         | Create, update, approve, revoke        |
| Assets         | Create, update, delete                 |
| Campaigns      | Create, update, approve, cancel        |
| Campaign Steps | Create, update, approve, status change |
| Actions        | Create, update                         |
| Evidence       | Upload, update, download, delete       |
| Findings       | Create, update, review, close          |
| Reports        | Generate, approve, download            |
| Telemetry      | Create, update, review                 |
| Approvals      | Request, approve, reject, revoke       |
| LLM Tasks      | Generate, review, accept, reject       |
| Imports        | Create, review                         |

---

## Security Notes

API implementation should include:

* Authentication
* Role-based access control
* Project membership check
* Scope validation
* Target allowlist validation
* Approval workflow
* File upload validation
* Evidence hash validation
* Audit logging
* Sensitive data sanitization
* Rate limiting
* Input validation
* Structured error handling

---

## Review Checklist

Use this checklist when reviewing API changes.

```text
[ ] Endpoint has a clear purpose
[ ] Request body is defined
[ ] Response body is defined
[ ] Authorization requirement is clear
[ ] Project membership is considered
[ ] Scope validation is considered
[ ] Approval requirement is considered
[ ] Audit event is defined
[ ] Sensitive data handling is considered
[ ] LLM output requires review when applicable
[ ] Error behavior is defined
[ ] Endpoint does not enable unauthorized execution
```

---

## Current Status

Current version:

```text
v0.1 Community Draft
```

Current focus:

```text
API structure
resource boundaries
request and response examples
scope validation
approval workflow
audit behavior
LLM-assisted workflow endpoints
future validation workflow boundary
```
