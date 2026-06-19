# LLM Assistance

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This document defines how LLM assistance is used in RedOps Framework.

LLM assistance supports planning, review, analysis, documentation, and reporting. It helps operators work with project scope, ATT&CK mapping, campaign planning, evidence, findings, telemetry, and reports.

LLM output must be validated before it affects project workflow.

---

## Operating Model

The framework separates LLM assistance from controlled validation workflow.

```text
User request
  |
  v
LLM assistance
  |
  v
Structured draft
  |
  v
Validation layer
  |
  |-- schema validation
  |-- ATT&CK registry validation
  |-- scope validation
  |-- policy validation
  |-- approval requirement
  |
  v
Human review
  |
  v
Accepted project artifact
```

Accepted project artifacts may include:

```text
scope summary
campaign plan draft
ATT&CK mapping suggestion
finding draft
report draft
telemetry review note
cleanup checklist
```

---

## Supported LLM Tasks

LLM assistance may be used for the following tasks.

| Task                   | Description                                                                        |
| ---------------------- | ---------------------------------------------------------------------------------- |
| Scope summary          | Summarize allowed targets, forbidden targets, test window, and restrictions        |
| ATT&CK mapping         | Suggest relevant ATT&CK tactics and techniques for a project objective             |
| Campaign plan draft    | Create a structured campaign draft from approved scope and objective               |
| Policy review          | Check whether a draft plan appears to conflict with scope or policy                |
| Evidence summary       | Summarize uploaded evidence, logs, screenshots, scanner output, or telemetry notes |
| Finding draft          | Draft title, summary, impact, likelihood, recommendation, and evidence references  |
| Remediation draft      | Suggest remediation language for confirmed findings                                |
| Report draft           | Draft executive summary, technical section, ATT&CK mapping, and limitation notes   |
| Telemetry gap analysis | Compare expected telemetry with observed telemetry                                 |
| Cleanup checklist      | Draft cleanup and revert checklist for controlled validation workflow              |
| Terminology review     | Improve consistency of terms used in documentation and reports                     |

---

## Restricted LLM Tasks

LLM assistance must not be used to directly perform the following tasks.

```text
direct_execution
scope_expansion_without_approval
approval_bypass
payload_generation
credential_theft
malware_generation
evasion_instruction
destructive_action
unauthorized_access_planning
out_of_scope_targeting
```

LLM output must not be treated as authorization.

LLM output must not override project scope, rules of engagement, approval requirements, or safety policy.

---

## LLM Roles

The framework defines four LLM roles.

| Role      | Purpose                                  | Output                                                  |
| --------- | ---------------------------------------- | ------------------------------------------------------- |
| Assistant | Summarize and explain project data       | Notes, summaries, review comments                       |
| Planner   | Draft structured project artifacts       | Campaign draft, ATT&CK mapping, checklist               |
| Analyst   | Review evidence, telemetry, and findings | Evidence summary, telemetry gap note, finding draft     |
| Reporter  | Draft report content                     | Executive summary, finding section, remediation section |

The LLM role must be selected based on the task.

---

## Assistant Mode

Assistant Mode supports reading, summarizing, and explaining project data.

Allowed tasks:

```text
summarize_scope
summarize_project
summarize_campaign_status
summarize_findings
summarize_evidence
explain_attack_mapping
explain_detection_status
```

Example output:

```yaml
task: summarize_scope
project_id: example-project
summary:
  allowed_targets:
    - app.example.com
    - 10.10.10.0/24
  forbidden_targets:
    - payment.example.com
  test_window: 2026-06-20T22:00:00Z to 2026-06-21T02:00:00Z
  approval_required: true
```

---

## Planner Mode

Planner Mode creates structured drafts from approved project data.

Planner Mode may suggest:

```text
campaign objective
ATT&CK tactic
ATT&CK technique
target asset
expected telemetry
approval requirement
evidence requirement
cleanup requirement
```

Planner Mode must not create direct execution commands.

Example campaign draft:

```yaml
task: campaign_plan_draft
project_id: example-project
objective: validate endpoint discovery telemetry
mode: validation
steps:
  - id: step-001
    tactic: Discovery
    technique_id: T1057
    technique_name: Process Discovery
    target_asset: lab-windows-01
    approval_required: true
    expected_telemetry:
      - process_creation
      - command_execution
    evidence_required:
      - telemetry_event
      - operator_note
    cleanup_required: false
```

Validation requirements:

```text
schema_validation
attack_registry_validation
scope_validation
policy_validation
human_review
```

---

## Analyst Mode

Analyst Mode reviews project evidence, telemetry, and finding data.

Allowed tasks:

```text
evidence_summary
scanner_result_summary
siem_alert_summary
edr_event_summary
telemetry_gap_analysis
finding_draft
finding_review_note
impact_summary
remediation_summary
```

Example telemetry review output:

```yaml
task: telemetry_gap_analysis
campaign_step_id: step-001
technique_id: T1057
expected_telemetry:
  - process_creation
  - command_execution
observed_telemetry:
  - process_creation
detection_status: partially_detected
gap:
  - command_execution telemetry was not observed
review_note: review endpoint logging configuration and detection rule coverage
```

---

## Reporter Mode

Reporter Mode drafts report sections from approved project data.

Allowed report sections:

```text
executive_summary
scope_summary
methodology_summary
campaign_summary
finding_summary
technical_finding
attack_mapping
detection_feedback
remediation_plan
limitations
cleanup_status
```

Example finding draft:

```yaml
task: finding_draft
finding:
  title: Endpoint discovery activity was not fully detected
  severity: medium
  affected_assets:
    - lab-windows-01
  attack_mapping:
    - technique_id: T1057
      technique_name: Process Discovery
  summary: Process discovery activity generated partial telemetry coverage.
  impact: Security monitoring may miss command execution context for endpoint discovery behavior.
  recommendation: Review endpoint logging configuration, detection rule coverage, and telemetry forwarding.
  evidence:
    - evidence-001
    - evidence-002
```

Finding drafts must be reviewed before inclusion in a report.

---

## Input Requirements

LLM tasks should use structured input when possible.

Recommended input fields:

```text
task
project_id
scope_ref
asset_ref
campaign_ref
campaign_step_ref
finding_ref
evidence_ref
attack_technique_ref
user_instruction
constraints
output_format
```

Example input:

```yaml
task: attack_mapping_suggestion
project_id: example-project
objective: review endpoint visibility for discovery behavior
scope_ref: scope-001
asset_ref:
  - lab-windows-01
constraints:
  mode: validation
  no_direct_execution: true
  output_format: yaml
```

---

## Output Requirements

LLM output should be structured and reviewable.

Required output properties:

```text
task
summary
references
assumptions
limitations
recommended_next_step
requires_review
```

For workflow-related output, add:

```text
project_id
scope_ref
target_ref
technique_id
risk_level
approval_required
expected_telemetry
evidence_required
cleanup_required
```

Example output envelope:

```yaml
task: campaign_plan_draft
requires_review: true
assumptions:
  - scope is already approved
  - target asset is in the allowlist
limitations:
  - output is a draft
  - approval is required before workflow execution
recommended_next_step: run scope and policy validation
content:
  objective: validate endpoint discovery telemetry
  steps:
    - id: step-001
      technique_id: T1057
      target_ref: lab-windows-01
      approval_required: true
```

---

## Validation Pipeline

LLM-generated output must pass validation before becoming a project artifact.

```text
LLM output
  |
  v
Format validation
  |
  v
Schema validation
  |
  v
ATT&CK registry validation
  |
  v
Scope validation
  |
  v
Policy validation
  |
  v
Human review
  |
  v
Project artifact
```

Validation checks:

| Check                      | Purpose                                                 |
| -------------------------- | ------------------------------------------------------- |
| Format validation          | Ensure output is valid Markdown, YAML, JSON, or text    |
| Schema validation          | Ensure required fields are present                      |
| ATT&CK registry validation | Ensure technique IDs and names match the local registry |
| Scope validation           | Ensure referenced assets are inside approved scope      |
| Policy validation          | Ensure risk level and approval requirement are correct  |
| Human review               | Ensure the output is accurate and appropriate           |

---

## Human Review

Human review is required before accepting LLM-generated output for:

```text
campaign_plan
restricted_action
finding
report
policy_exception
scope_change
telemetry_gap_conclusion
cleanup_completion
```

Reviewer responsibilities:

1. Check scope alignment.
2. Check target references.
3. Check ATT&CK mapping.
4. Check severity and impact language.
5. Check evidence references.
6. Check assumptions.
7. Check limitations.
8. Remove unsupported claims.
9. Confirm approval requirement.
10. Confirm report readiness.

---

## Prompt Boundary

Prompts should keep the LLM inside the project workflow.

Prompt requirements:

```text
state the task
state the project context
state the approved scope
state the output format
state the safety constraints
state what the model must not do
request assumptions and limitations
request reviewable output
```

Example prompt:

```text
Task: Draft a campaign plan.
Project: example-project.
Scope: use only assets listed in scope-001.
Objective: validate endpoint discovery telemetry.
Constraints: no direct execution, no exploit steps, no credential access, no evasion, no destructive action.
Output: YAML.
Include: ATT&CK technique, target reference, expected telemetry, evidence requirement, approval requirement, cleanup requirement, assumptions, and limitations.
```

---

## Prompt Safety Rules

Prompt rules:

1. Use approved project context.
2. Use explicit scope references.
3. Use structured output.
4. Require assumptions.
5. Require limitations.
6. Require review status.
7. Do not ask for direct execution commands.
8. Do not ask for payload generation.
9. Do not ask for evasion.
10. Do not ask for credential theft.
11. Do not ask for destructive actions.
12. Do not ask the LLM to bypass policy.

---

## Data Handling

LLM tasks should use the minimum data required.

Do not send the following data to an LLM unless explicitly approved and protected:

```text
credentials
tokens
private_keys
client_confidential_data
raw_production_logs
sensitive_siem_exports
sensitive_edr_exports
private_network_maps
personal_data
regulated_data
```

Data handling requirements:

1. Use sanitized examples where possible.
2. Remove secrets from evidence before analysis.
3. Avoid raw production logs when summary data is enough.
4. Track which project artifacts were generated or assisted by LLM.
5. Record reviewer identity for accepted LLM output.

---

## Audit Requirements

Audit log should record accepted LLM-assisted changes.

Audit events:

```text
llm_task_requested
llm_output_generated
llm_output_reviewed
llm_output_accepted
llm_output_rejected
llm_assisted_finding_created
llm_assisted_report_created
llm_assisted_campaign_draft_created
```

Audit fields:

```text
audit_id
project_id
actor_id
llm_task
entity_type
entity_id
model_provider
output_hash
reviewer_id
status
created_at
```

The audit log should not store sensitive prompts or raw outputs when they contain restricted data.

---

## Review Checklist

Use this checklist before accepting LLM-generated output.

```text
[ ] Output matches requested format
[ ] Output references approved project
[ ] Output references approved scope
[ ] Output references allowed target
[ ] ATT&CK technique ID is valid
[ ] Risk level is correct
[ ] Approval requirement is correct
[ ] Evidence requirement is defined
[ ] Cleanup requirement is defined when needed
[ ] No unsupported claim is present
[ ] No restricted content is present
[ ] Assumptions are listed
[ ] Limitations are listed
[ ] Human reviewer is assigned
[ ] Audit event is recorded
```

---

## Integration Points

LLM assistance may integrate with the following framework components:

| Component         | LLM Use                                   |
| ----------------- | ----------------------------------------- |
| Project Workspace | Summarize project status                  |
| Scope Manager     | Summarize scope and identify restrictions |
| Asset Registry    | Summarize asset context                   |
| ATT&CK Registry   | Suggest tactic and technique mapping      |
| Campaign Planner  | Draft campaign plan                       |
| Action Log        | Summarize operator activity               |
| Evidence Vault    | Summarize evidence                        |
| Finding Manager   | Draft and review findings                 |
| Report Builder    | Draft report sections                     |
| Safety Gate       | Review policy alignment                   |
| Telemetry Model   | Summarize detection gaps                  |

---

## Failure Modes

Known failure modes:

| Failure Mode             | Risk                          | Control                            |
| ------------------------ | ----------------------------- | ---------------------------------- |
| Incorrect ATT&CK mapping | Wrong technique reference     | Registry validation                |
| Scope mismatch           | Out-of-scope target reference | Scope validation                   |
| Unsupported claim        | Inaccurate finding or report  | Human review                       |
| Missing limitation       | Overstated result             | Required limitation field          |
| Sensitive data exposure  | Data leakage                  | Data minimization and sanitization |
| Unsafe plan suggestion   | Misuse risk                   | Policy validation                  |
| Approval bypass          | Unauthorized workflow         | Approval gate                      |
| Ambiguous output         | Review difficulty             | Structured output requirement      |

---

## Version Scope

Current version:

```text
v0.1 Community Draft
```

Current scope:

```text
LLM-assisted planning
LLM-assisted review
LLM-assisted evidence summary
LLM-assisted finding draft
LLM-assisted report draft
LLM output validation
LLM safety boundary
```

Future versions may define implementation-specific APIs, prompt templates, and model provider configuration.
