# Telemetry Model

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This document defines the telemetry model for RedOps Framework.

The telemetry model stores expected telemetry, observed telemetry, detection status, evidence reference, and review notes for campaign steps, validation workflow, findings, and reports.

Telemetry review helps teams understand whether planned activity produced the expected detection signal.

---

## Scope

The telemetry model covers:

* Expected telemetry
* Observed telemetry
* Detection status
* Data source reference
* Evidence reference
* ATT&CK technique mapping
* Detection gap note
* Reviewer workflow
* Report output

Early versions should store telemetry as manually reviewed project data.

Future versions may support SIEM, EDR, cloud logging, and detection engineering integrations.

---

## Core Concepts

| Concept            | Description                                                             |
| ------------------ | ----------------------------------------------------------------------- |
| Expected Telemetry | Signal expected from a campaign step or validation workflow             |
| Observed Telemetry | Signal found in logs, alerts, EDR events, SIEM events, or manual review |
| Detection Status   | Review result for expected and observed telemetry                       |
| Data Source        | System that produced the signal                                         |
| Evidence Reference | Evidence file or record linked to observed telemetry                    |
| Detection Gap      | Missing, incomplete, delayed, or low-quality telemetry                  |
| Reviewer Note      | Human review note for detection result                                  |
| ATT&CK Mapping     | Technique reference related to telemetry                                |

---

## Detection Status Values

```text
unknown
detected
not_detected
blocked
partially_detected
not_applicable
```

| Status               | Meaning                                                           |
| -------------------- | ----------------------------------------------------------------- |
| `unknown`            | Telemetry has not been reviewed                                   |
| `detected`           | Expected telemetry was observed and linked to evidence            |
| `not_detected`       | Expected telemetry was not observed                               |
| `blocked`            | Activity was blocked before expected telemetry could be completed |
| `partially_detected` | Some expected telemetry was observed, but coverage was incomplete |
| `not_applicable`     | Telemetry review does not apply to this step                      |

---

## Telemetry Record

Telemetry record fields:

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

Required fields:

```text
project_id
detection_status
created_at
```

Recommended fields:

```text
campaign_step_id
asset_id
attack_technique_id
expected_telemetry
observed_telemetry
data_source
evidence_id
review_note
reviewed_by
reviewed_at
```

---

## Expected Telemetry

Expected telemetry describes what should be visible if the activity is logged or detected.

Expected telemetry fields:

```text
name
description
data_source
data_component
signal
required
```

Example:

```yaml
expected_telemetry:
  - name: process creation event
    data_source: endpoint
    data_component: Process Creation
    signal: process execution related to process discovery
    required: true
```

Rules:

1. Expected telemetry should be defined before validation.
2. Expected telemetry should reference a data source.
3. Expected telemetry should reference an ATT&CK technique when applicable.
4. Required telemetry should be reviewed before step completion.
5. Missing required telemetry should create a detection gap note.

---

## Observed Telemetry

Observed telemetry describes what was found during review.

Observed telemetry fields:

```text
name
description
data_source
data_component
signal
required
```

Example:

```yaml
observed_telemetry:
  - name: endpoint process creation
    data_source: edr
    data_component: Process Creation
    signal: event matched the expected process creation signal
    required: false
```

Confidence values:

```text
low
medium
high
manual_review_required
```

---

## Data Source Types

Supported data source types:

```text
endpoint
siem
edr
network
firewall
proxy
dns
identity
cloud
application
database
scanner
manual_review
other
```

Data source fields:

```text
data_source_id
project_id
name
type
owner
description
retention_period
review_method
notes
```

Example:

```yaml
data_source:
  name: endpoint-edr
  type: edr
  owner: detection-engineering
  review_method: manual export
```

---

## ATT&CK Data Component Mapping

Telemetry may map to ATT&CK data components.

Mapping fields:

```text
attack_technique_id
data_component
expected_signal
observed_signal
detection_status
evidence_id
reviewed_by
reviewed_at
```

Example:

```yaml
attack_mapping:
  attack_technique_id: T1057
  technique_name: Process Discovery
  data_component: Process Creation
  detection_status: partially_detected
  evidence_id: evidence-001
```

Rules:

1. Data component mapping should use the local ATT&CK Registry.
2. Invalid ATT&CK IDs should be rejected.
3. Deprecated techniques should show a warning.
4. Revoked techniques should not be used for new telemetry mapping.
5. LLM-generated telemetry mapping requires validation.

---

## Campaign Step Telemetry

Campaign steps may define expected telemetry.

Campaign step telemetry fields:

```text
campaign_step_id
attack_technique_id
target_asset_id
expected_telemetry
detection_status
telemetry_required
review_status
```

Example:

```yaml
campaign_step:
  id: step-001
  technique_id: T1057
  target_asset: lab-windows-01
  expected_telemetry:
    - process_creation
    - command_execution
  telemetry_required: true
  detection_status: unknown
```

Review rules:

1. A campaign step may be completed without telemetry review only if telemetry is not required.
2. A campaign step with required telemetry should stay in review until detection status is recorded.
3. `not_detected` and `partially_detected` should create review notes.
4. Detection status should be included in report output.

---

## Finding Telemetry

Findings may include telemetry data.

Finding telemetry use cases:

* Detection gap finding
* Missing log source finding
* Incomplete detection finding
* Delayed alert finding
* Control coverage finding

Finding telemetry fields:

```text
finding_id
attack_technique_id
expected_telemetry
observed_telemetry
detection_status
gap_summary
evidence_id
reviewed_by
reviewed_at
```

Example:

```yaml
finding_telemetry:
  finding_id: finding-001
  technique_id: T1057
  detection_status: partially_detected
  gap_summary: command execution telemetry was not available during review
  evidence_id: evidence-001
```

---

## Detection Gap Model

Detection gaps describe missing or incomplete telemetry.

Detection gap types:

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

Detection gap fields:

```text
gap_id
project_id
campaign_step_id
finding_id
attack_technique_id
gap_type
summary
impact
recommendation
evidence_id
created_by
created_at
```

Example:

```yaml
detection_gap:
  gap_type: incomplete_telemetry
  technique_id: T1057
  summary: process creation telemetry was observed, but command execution context was not available
  impact: investigation context may be incomplete
  recommendation: review endpoint logging policy and SIEM parsing
```

---

## Review Workflow

Telemetry review workflow:

```text
Define expected telemetry
  |
  v
Record action or validation result
  |
  v
Collect or attach evidence
  |
  v
Review observed telemetry
  |
  v
Assign detection status
  |
  v
Create detection gap when needed
  |
  v
Link telemetry to finding or report
```

Review status values:

```text
not_started
in_review
reviewed
requires_follow_up
closed
```

Reviewer responsibilities:

1. Check expected telemetry.
2. Check evidence reference.
3. Check observed telemetry.
4. Assign detection status.
5. Record limitations.
6. Create detection gap when needed.
7. Link telemetry to finding when relevant.
8. Approve telemetry section for report output.

---

## Evidence Relationship

Telemetry records should link to evidence when observed data is available.

Evidence examples:

```text
siem_alert
edr_alert
log_file
screenshot
scanner_output
manual_note
configuration_export
```

Rules:

1. Observed telemetry should reference evidence.
2. Evidence must belong to the same project.
3. Evidence access must follow project membership.
4. Evidence containing sensitive data should be marked restricted.
5. Evidence hash should be stored when the evidence is a file.

---

## LLM-Assisted Telemetry Review

LLM assistance may support telemetry review.

Allowed LLM tasks:

```text
summarize_observed_telemetry
compare_expected_and_observed_telemetry
draft_detection_gap_note
draft_report_detection_feedback
draft_remediation_language
```

Restricted LLM tasks:

```text
generate_evasion_steps
generate_detection_bypass
modify_detection_status_without_review
accept_telemetry_without_evidence
expand_scope
override_policy
```

LLM output must include:

```text
summary
assumptions
limitations
evidence_references
recommended_detection_status
requires_review
```

Example:

```yaml
task: telemetry_gap_analysis
campaign_step_id: step-001
technique_id: T1057
expected_telemetry:
  - process_creation
  - command_execution
observed_telemetry:
  - process_creation
recommended_detection_status: partially_detected
limitations:
  - command execution telemetry was not available in the reviewed evidence
requires_review: true
```

---

## Report Output

Telemetry data may appear in report sections.

Report sections:

```text
Detection Feedback
ATT&CK Mapping
Technical Findings
Evidence Appendix
Limitations
Remediation Plan
```

Recommended report fields:

```text
attack_id
technique_name
asset
expected_telemetry
observed_telemetry
detection_status
gap_summary
evidence_reference
recommendation
```

Example report row:

| ATT&CK ID | Technique         | Asset          | Detection Status   | Evidence     |
| --------- | ----------------- | -------------- | ------------------ | ------------ |
| T1057     | Process Discovery | lab-windows-01 | partially_detected | evidence-001 |

---

## Metrics

Telemetry review may support project metrics.

Suggested metrics:

| Metric                    | Description                                        |
| ------------------------- | -------------------------------------------------- |
| Expected telemetry count  | Number of expected telemetry items                 |
| Observed telemetry count  | Number of observed telemetry items                 |
| Detection rate            | Percentage of steps marked detected                |
| Partial detection rate    | Percentage of steps marked partially detected      |
| Not detected count        | Number of steps marked not detected                |
| Missing data source count | Number of gaps caused by unavailable data source   |
| Evidence coverage         | Percentage of telemetry records linked to evidence |
| Review completion         | Percentage of telemetry records reviewed           |

Metrics should be treated as project review indicators. They should not replace human analysis.

---

## API Proposal

Initial telemetry endpoints:

```http
GET    /api/v1/projects/{project_id}/telemetry
POST   /api/v1/projects/{project_id}/telemetry
PATCH  /api/v1/projects/{project_id}/telemetry/{telemetry_id}
```

Detection gap endpoints:

```http
GET    /api/v1/projects/{project_id}/detection-gaps
POST   /api/v1/projects/{project_id}/detection-gaps
PATCH  /api/v1/projects/{project_id}/detection-gaps/{gap_id}
```

---

## Schema Draft

Telemetry schema draft:

```json
{
  "telemetry_id": "telemetry-001",
  "project_id": "project-001",
  "campaign_step_id": "step-001",
  "asset_id": "asset-001",
  "attack_technique_id": "T1057",
  "expected_telemetry": [
    "process_creation",
    "command_execution"
  ],
  "observed_telemetry": [
    "process_creation"
  ],
  "data_source": "edr",
  "detection_status": "partially_detected",
  "evidence_id": "evidence-001",
  "review_note": "command execution context was not available",
  "reviewed_by": "reviewer-001",
  "reviewed_at": "2026-06-20T15:00:00Z"
}
```

Detection gap schema draft:

```json
{
  "gap_id": "gap-001",
  "project_id": "project-001",
  "campaign_step_id": "step-001",
  "attack_technique_id": "T1057",
  "gap_type": "incomplete_telemetry",
  "summary": "Process creation telemetry was observed, but command execution context was not available.",
  "impact": "Investigation context may be incomplete.",
  "recommendation": "Review endpoint logging policy, EDR configuration, and SIEM parsing.",
  "evidence_id": "evidence-001"
}
```

---

## Review Checklist

Use this checklist when reviewing telemetry records.

```text
[ ] Expected telemetry is defined
[ ] Observed telemetry is documented
[ ] Data source is identified
[ ] ATT&CK technique mapping is valid
[ ] Evidence is linked
[ ] Detection status is assigned
[ ] Review note is present
[ ] Gaps are documented
[ ] Sensitive data is removed or restricted
[ ] Report output is accurate
[ ] LLM-generated summary has been reviewed
```

---

## Current Status

Current version:

```text
v0.1 Community Draft
```

Current focus:

```text
expected telemetry
observed telemetry
detection status
detection gap
evidence reference
report output
LLM-assisted review
```
