# ATT&CK Registry

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This document defines the ATT&CK Registry model for RedOps Framework.

The registry stores ATT&CK tactics, techniques, sub-techniques, relationships, platforms, data components, mitigations, references, and content version metadata.

The registry is used by campaign planning, finding mapping, telemetry review, reporting, and LLM-assisted workflows.

---

## Scope

The ATT&CK Registry covers:

* ATT&CK content import
* Tactic model
* Technique model
* Sub-technique model
* Relationship model
* Version-aware mapping
* Detection and telemetry mapping
* Campaign step mapping
* Finding mapping
* Report mapping
* LLM output validation

Early versions should focus on Enterprise ATT&CK.

Future versions may add Mobile ATT&CK and ICS ATT&CK.

---

## Registry Goals

The registry should support:

1. Local ATT&CK lookup.
2. Version-aware technique mapping.
3. Campaign planning with ATT&CK references.
4. Finding mapping to ATT&CK techniques.
5. Telemetry expectation mapping.
6. Report output with ATT&CK coverage.
7. LLM-generated mapping validation.
8. Detection feedback and coverage review.
9. Deprecated and revoked technique handling.
10. Repeatable data import from ATT&CK STIX.

---

## Source Data

Primary source:

```text id="4v6ihq"
MITRE ATT&CK STIX data
```

Initial dataset:

```text id="givqdh"
enterprise-attack.json
```

Future datasets:

```text id="3xqdkb"
mobile-attack.json
ics-attack.json
```

The registry should store import metadata for every ATT&CK dataset.

Import metadata fields:

```text id="0detgp"
import_id
domain
source_file
source_url
content_version
imported_by
imported_at
object_count
status
notes
```

---

## ATT&CK Domains

Supported domain values:

```text id="3b7xxs"
enterprise
mobile
ics
```

Initial implementation target:

```text id="j0uwl6"
enterprise
```

Domain support should be explicit. A technique from one domain should not be treated as equivalent to a technique from another domain unless a mapping is defined.

---

## Core Entities

Registry entities:

```text id="kttnvi"
attack_collection
attack_tactic
attack_technique
attack_relationship
attack_data_component
attack_mitigation
attack_reference
attack_import_log
```

Optional future entities:

```text id="6p9ewb"
attack_group
attack_software
attack_campaign
attack_procedure
attack_flow_mapping
```

---

## Collection Model

The collection model stores ATT&CK dataset metadata.

Fields:

```text id="s04v6y"
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

Example:

```yaml id="vc8f2t"
collection:
  domain: enterprise
  name: Enterprise ATT&CK
  content_version: "unknown"
  source: attack-stix-data
  imported_at: "2026-01-01T00:00:00Z"
```

The actual content version should come from the imported ATT&CK dataset.

---

## Tactic Model

Tactics describe the tactical objective of an action.

Fields:

```text id="hr1q03"
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

```yaml id="j8xr6i"
tactic:
  attack_id: TA0007
  short_name: discovery
  name: Discovery
  domain: enterprise
  content_version: "unknown"
```

Tactic records should be linked to techniques through ATT&CK relationships or technique kill chain phase metadata.

---

## Technique Model

Techniques describe how a tactical objective may be achieved.

Fields:

```text id="8s64wu"
technique_id
attack_id
name
description
domain
tactics
platforms
permissions_required
effective_permissions
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

```text id="cg9gq9"
attack_id
name
domain
content_version
revoked
deprecated
```

Optional fields:

```text id="unltfy"
description
platforms
data_components
detection
mitigations
references
raw_stix
```

Example:

```yaml id="88niss"
technique:
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
  content_version: "unknown"
  revoked: false
  deprecated: false
```

---

## Sub-Technique Model

Sub-techniques are stored in the same table as techniques.

Sub-technique rules:

1. `is_subtechnique` must be `true`.
2. `parent_attack_id` must reference a parent technique.
3. A sub-technique should inherit domain from the parent technique.
4. A sub-technique should not replace the parent technique.
5. Campaign steps may reference either a technique or a sub-technique.

Example:

```yaml id="u9yioo"
technique:
  attack_id: T1053.005
  name: Scheduled Task
  domain: enterprise
  tactics:
    - persistence
    - privilege-escalation
    - execution
  is_subtechnique: true
  parent_attack_id: T1053
  content_version: "unknown"
  revoked: false
  deprecated: false
```

---

## Relationship Model

Relationships connect ATT&CK objects.

Relationship fields:

```text id="x4dbw7"
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

Common relationship types:

```text id="r974wz"
uses
mitigates
detects
subtechnique-of
revoked-by
related-to
```

Relationship use cases:

| Relationship                      | Use                                      |
| --------------------------------- | ---------------------------------------- |
| technique to tactic               | Campaign planning and coverage mapping   |
| sub-technique to parent technique | Registry navigation                      |
| mitigation to technique           | Finding recommendation and report output |
| data component to technique       | Telemetry expectation mapping            |
| revoked technique to replacement  | Migration and warning                    |
| software or group to technique    | Future threat-informed prioritization    |

---

## Data Component Model

Data components describe expected telemetry or observable data.

Fields:

```text id="axml9t"
data_component_id
name
description
domain
related_techniques
content_version
references
```

Use cases:

* Define expected telemetry for campaign steps.
* Map observed telemetry to ATT&CK techniques.
* Support detection validation.
* Support report detection feedback.
* Validate LLM-generated telemetry suggestions.

Example:

```yaml id="3z69zi"
data_component:
  name: Process Creation
  domain: enterprise
  related_techniques:
    - T1057
```

---

## Mitigation Model

Mitigations describe defensive controls or recommendations related to techniques.

Fields:

```text id="y98vc7"
mitigation_id
attack_id
name
description
domain
related_techniques
content_version
references
```

Use cases:

* Support finding recommendations.
* Support report remediation sections.
* Support control mapping.
* Support security review workflow.

Example:

```yaml id="639f4m"
mitigation:
  attack_id: M1047
  name: Audit
  domain: enterprise
  related_techniques:
    - T1057
```

---

## Reference Model

References store source links and external references from ATT&CK.

Fields:

```text id="ym2f6h"
reference_id
source_name
url
description
external_id
related_object_id
domain
content_version
```

Rules:

1. References should be preserved from source data.
2. References should be linked to the related ATT&CK object.
3. References should not be used as proof that a campaign step was executed.
4. Report output may include ATT&CK references when needed.

---

## Version-Aware Registry

ATT&CK content changes over time.

The registry should store content version with every imported object.

Recommended identity key:

```text id="f2cuvq"
domain + attack_id + content_version
```

Example:

```text id="2ss16j"
enterprise:T1057:content_version
```

Version-aware behavior:

1. Store the imported content version.
2. Store source creation timestamp.
3. Store source modification timestamp.
4. Preserve deprecated status.
5. Preserve revoked status.
6. Do not delete old mappings automatically.
7. Keep historical project mappings stable.
8. Warn when a mapped technique becomes deprecated or revoked.
9. Support migration review when content changes.

---

## Deprecated and Revoked Handling

Deprecated and revoked objects should remain in the registry.

Handling rules:

| Status     | Registry Behavior                                    |
| ---------- | ---------------------------------------------------- |
| Active     | Can be used in campaign planning and finding mapping |
| Deprecated | Can be displayed with warning                        |
| Revoked    | Should not be used for new campaign steps            |
| Replaced   | Should suggest replacement when available            |

Campaign Planner behavior:

1. Allow active techniques.
2. Warn on deprecated techniques.
3. Block revoked techniques for new campaign steps.
4. Preserve revoked techniques in historical records.
5. Show replacement reference when available.

---

## Import Flow

ATT&CK import flow:

```text id="qkxepm"
Load STIX bundle
  |
  v
Read collection metadata
  |
  v
Extract tactics
  |
  v
Extract techniques and sub-techniques
  |
  v
Extract relationships
  |
  v
Extract mitigations
  |
  v
Extract data components
  |
  v
Extract references
  |
  v
Normalize objects
  |
  v
Upsert registry records
  |
  v
Record import log
```

---

## Import Rules

Import rules:

1. Validate source format before import.
2. Import one domain at a time.
3. Preserve source IDs.
4. Preserve source timestamps.
5. Preserve source references.
6. Preserve raw object when needed for audit.
7. Upsert by domain, ATT&CK ID, and content version.
8. Mark missing objects as unchanged until a migration review is performed.
9. Do not remove historical project mappings.
10. Record import summary.

Import status values:

```text id="tp222v"
pending
running
completed
failed
completed_with_warnings
```

Import log fields:

```text id="bdiafc"
import_id
domain
content_version
source_file
source_url
started_at
completed_at
status
object_count
created_count
updated_count
warning_count
error_count
notes
```

---

## Registry Search

Search should support:

```text id="88m8pw"
attack_id
technique_name
tactic
platform
domain
content_version
is_subtechnique
deprecated
revoked
```

Example query parameters:

```text id="n9sdpa"
?attack_id=T1057
?tactic=discovery
?platform=Windows
?domain=enterprise
?is_subtechnique=true
?deprecated=false
?revoked=false
```

Search result fields:

```text id="ydb8tg"
attack_id
name
domain
tactics
platforms
is_subtechnique
parent_attack_id
content_version
deprecated
revoked
```

---

## Campaign Mapping

Campaign steps may reference ATT&CK techniques.

Campaign step mapping fields:

```text id="a3bg1l"
campaign_step_id
attack_technique_id
attack_id
domain
content_version
mapping_note
mapped_by
mapped_at
```

Mapping rules:

1. Technique must exist in the registry.
2. Technique must match the selected domain.
3. Technique should not be revoked.
4. Deprecated technique requires warning.
5. Content version must be stored with the mapping.
6. LLM-suggested mapping requires validation.
7. Manual override should be logged.

---

## Finding Mapping

Findings may reference ATT&CK techniques.

Finding mapping fields:

```text id="m5jjk7"
finding_id
attack_technique_id
attack_id
domain
content_version
mapping_confidence
mapping_note
mapped_by
reviewed_by
mapped_at
```

Mapping confidence values:

```text id="mu9g09"
low
medium
high
manual_review_required
```

Finding mapping rules:

1. Mapping must be reviewable.
2. Mapping confidence should be recorded.
3. Evidence should support the mapping.
4. Deprecated mapping should show a warning.
5. Revoked mapping should require reviewer confirmation if historical data depends on it.

---

## Telemetry Mapping

Telemetry mapping links campaign steps and findings to expected or observed data.

Telemetry mapping fields:

```text id="o2ip2z"
telemetry_id
project_id
campaign_step_id
finding_id
attack_technique_id
expected_telemetry
observed_telemetry
data_component
data_source
detection_status
evidence_id
reviewed_by
reviewed_at
```

Detection status values:

```text id="y2ovmu"
unknown
detected
not_detected
blocked
partially_detected
not_applicable
```

Telemetry mapping rules:

1. Expected telemetry should be defined before validation.
2. Observed telemetry should reference evidence.
3. Detection status should be reviewed.
4. Missing telemetry should be documented.
5. Detection feedback should be available for report output.

---

## LLM Validation

LLM-assisted ATT&CK mapping must be validated against the registry.

LLM output should include:

```text id="t20eep"
task
project_id
scope_ref
objective
suggested_tactics
suggested_techniques
assumptions
limitations
requires_review
```

Validation checks:

| Check                     | Purpose                              |
| ------------------------- | ------------------------------------ |
| ATT&CK ID exists          | Prevent invalid technique IDs        |
| Domain match              | Prevent cross-domain mismatch        |
| Content version available | Preserve mapping consistency         |
| Revoked status            | Prevent new use of revoked technique |
| Deprecated status         | Show warning                         |
| Scope alignment           | Check that target context is allowed |
| Reviewer approval         | Accept or reject mapping             |

Example LLM mapping draft:

```yaml id="d8sdsu"
task: attack_mapping_suggestion
project_id: example-project
objective: review endpoint discovery visibility
suggested_techniques:
  - attack_id: T1057
    name: Process Discovery
    domain: enterprise
    reason: endpoint discovery activity may create process and command telemetry
requires_review: true
```

---

## Report Usage

Reports may include ATT&CK data for:

* Campaign mapping
* Finding mapping
* Detection feedback
* Coverage summary
* Technique references
* Mitigation references
* Limitations

Report output should include:

```text id="13noaa"
attack_id
technique_name
tactic
domain
content_version
mapping_note
evidence_reference
detection_status
```

Reports should not imply that a technique was fully emulated when only mapping or documentation was performed.

---

## API Proposal

Initial API endpoints:

```http id="wmh3gr"
POST /api/v1/attack/import
GET  /api/v1/attack/collections
GET  /api/v1/attack/tactics
GET  /api/v1/attack/techniques
GET  /api/v1/attack/techniques/{technique_id}
GET  /api/v1/attack/search
GET  /api/v1/attack/imports
GET  /api/v1/attack/imports/{import_id}
```

Mapping endpoints:

```http id="a5m9ka"
POST /api/v1/campaign-steps/{step_id}/attack-mapping
POST /api/v1/findings/{finding_id}/attack-mapping
POST /api/v1/telemetry/{telemetry_id}/attack-mapping
```

---

## Schema Draft

Technique schema draft:

```json id="em7wyo"
{
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

Mapping schema draft:

```json id="pv08g9"
{
  "entity_type": "campaign_step",
  "entity_id": "step-001",
  "attack_id": "T1057",
  "domain": "enterprise",
  "content_version": "unknown",
  "mapping_note": "Mapped to endpoint discovery visibility review.",
  "requires_review": true
}
```

---

## Review Checklist

Use this checklist when reviewing ATT&CK registry changes:

```text id="d9my93"
[ ] Source dataset is identified
[ ] Domain is identified
[ ] Content version is stored
[ ] Technique IDs are preserved
[ ] Tactics are mapped
[ ] Sub-techniques reference parent techniques
[ ] Deprecated status is preserved
[ ] Revoked status is preserved
[ ] References are preserved
[ ] Import log is created
[ ] Historical mappings are not deleted
[ ] LLM-generated mappings require validation
[ ] Report output includes content version
```

---

## Current Status

Current version:

```text id="2gpqxk"
v0.1 Community Draft
```

Current focus:

```text id="lr4y16"
ATT&CK registry model
version-aware mapping
campaign mapping
finding mapping
telemetry mapping
LLM mapping validation
```
