# Glossary

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This document defines common terms used in RedOps Framework.

The glossary helps keep documentation, schemas, templates, and future implementation work consistent.

---

## Core Terms

### Action

An operator record that describes work performed during a project.

Examples:

* Manual validation note
* Configuration review note
* Scanner result note
* Detection validation note
* Cleanup note

---

### Action Log

A project record that stores operator activity, result, detection status, timestamp, and linked evidence.

---

### Admin

A user role with permission to manage users, roles, system settings, ATT&CK import, and global configuration.

---

### Approval

A review record required before controlled, sensitive, or high-risk workflow is accepted.

Approval status values:

```text
not_required
pending
approved
rejected
expired
revoked
```

---

### Asset

A target object that belongs to a project.

Examples:

* IP address
* IP range
* Domain
* Subdomain
* URL
* Cloud account
* Repository
* Application
* API
* Identity tenant
* Lab environment

---

### Asset Registry

A module that stores project assets and related metadata.

---

### ATT&CK

MITRE ATT&CK is used as a reference model for tactics, techniques, sub-techniques, platforms, data components, mitigations, and references.

---

### ATT&CK Mapping

The process of linking a campaign step, finding, telemetry record, or report section to an ATT&CK tactic or technique.

---

### ATT&CK Registry

A local model that stores ATT&CK tactics, techniques, sub-techniques, relationships, content version, references, deprecated status, and revoked status.

---

### Audit Log

A record of important project or system activity.

Examples:

* Scope approval
* Campaign creation
* Evidence upload
* Finding review
* Report generation
* LLM output acceptance

---

### Audit Trail

The collection of audit logs that supports review and accountability.

---

## Campaign Terms

### Campaign

A planned set of activities for a project.

A campaign includes objective, assumptions, ATT&CK mapping, campaign steps, approval status, and result tracking.

---

### Campaign Planner

A module used to create and manage campaign plans.

---

### Campaign Step

An individual planned step inside a campaign.

A campaign step may reference:

* ATT&CK technique
* Target asset
* Expected result
* Expected telemetry
* Approval requirement
* Evidence requirement

---

### Campaign Status

Allowed campaign status values:

```text
draft
pending_approval
approved
in_progress
completed
cancelled
```

---

### Campaign Step Status

Allowed campaign step status values:

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

## Detection and Telemetry Terms

### Data Component

A type of observable data related to an ATT&CK technique.

Examples:

* Process Creation
* Command Execution
* File Access
* Network Connection
* Authentication Event

---

### Data Source

A system or log source that provides telemetry.

Examples:

* EDR
* SIEM
* Firewall
* Proxy
* DNS
* Identity provider
* Cloud logging
* Application log

---

### Detection Gap

A missing, incomplete, delayed, or low-confidence detection result.

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

---

### Detection Status

The review result for expected and observed telemetry.

Allowed values:

```text
unknown
detected
not_detected
blocked
partially_detected
not_applicable
```

---

### Expected Telemetry

The signal that should be visible after a campaign step or validation workflow.

---

### Observed Telemetry

The signal that was found during review.

Observed telemetry should reference evidence when available.

---

### Telemetry

Detection or observation data related to a project, campaign step, asset, finding, or report.

---

### Telemetry Model

A model that stores expected telemetry, observed telemetry, data source, detection status, evidence reference, and review notes.

---

### Telemetry Review

The process of comparing expected telemetry with observed telemetry.

---

## Evidence and Finding Terms

### Evidence

A file or record that supports an action, telemetry review, or finding.

Examples:

* Screenshot
* Terminal output
* Log file
* HTTP request and response
* Scanner output
* SIEM alert
* EDR alert
* Manual note

---

### Evidence Integrity

The requirement to store evidence metadata and integrity data.

Expected metadata:

* File name
* File size
* MIME type
* SHA256 hash
* Uploader
* Upload time
* Project reference

---

### Evidence Vault

A module that stores evidence files and metadata.

---

### Finding

A documented security issue, weakness, observation, or detection gap.

A finding may include:

* Title
* Summary
* Severity
* Affected assets
* ATT&CK mapping
* Evidence references
* Impact
* Likelihood
* Recommendation
* Review status

---

### Finding Manager

A module that stores findings and related evidence.

---

### Finding Status

Allowed finding status values:

```text
draft
under_review
confirmed
risk_accepted
remediated
closed
```

---

### Severity

A rating used to describe finding impact.

Allowed values:

```text
informational
low
medium
high
critical
```

---

## LLM Terms

### LLM Assistance

A support layer that helps with planning, review, analysis, and documentation.

Supported tasks:

* Scope summary
* ATT&CK mapping suggestion
* Campaign plan draft
* Evidence summary
* Finding draft
* Report draft
* Telemetry gap analysis
* Cleanup checklist

---

### LLM Output

Text or structured data generated by an LLM.

LLM output must be reviewed before it becomes a project artifact.

---

### LLM Task

A tracked request for LLM assistance.

Example task types:

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

---

### Planner Mode

An LLM mode used to draft structured project artifacts such as campaign plans and ATT&CK mapping suggestions.

---

### Analyst Mode

An LLM mode used to summarize evidence, review telemetry, and draft findings.

---

### Reporter Mode

An LLM mode used to draft report sections.

---

### Human Review

A required review step before accepting LLM-generated output for project use.

---

## Project and Scope Terms

### Client Viewer

A user role that can view finalized report output and approved summaries.

---

### Engagement

An authorized security assessment or operation.

Examples:

* External pentest
* Internal pentest
* Web application pentest
* Red team engagement
* Purple team exercise
* Internal assessment

---

### Engagement Type

The category of project.

Allowed values:

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

---

### Forbidden Target

A target that must not be used in campaign planning, action logs, validation workflow, or reporting as an approved test target.

---

### Lead Operator

A user role that can create projects, define scope, plan campaigns, approve restricted actions, review findings, and generate reports.

---

### Operator

A user role that can record actions, upload evidence, create findings, and update campaign status.

---

### Project

The main workspace for an engagement.

A project links to:

* Scope
* Assets
* Campaigns
* Actions
* Evidence
* Findings
* Reports
* Telemetry
* Audit logs
* Members

---

### Project Workspace

A module that stores engagement-level information and links project artifacts.

---

### Reviewer

A user role that reviews evidence, findings, report content, and safety alignment.

---

### Rules of Engagement

The approved rules that define what is allowed, restricted, and forbidden in a project.

---

### Scope

The approved boundary of a project.

Scope includes:

* Allowed targets
* Forbidden targets
* Test window
* Rules of engagement
* Restricted actions
* Approval requirement
* Emergency contact

---

### Scope Manager

A module that stores and manages project scope.

---

### Scope Status

Allowed scope status values:

```text
draft
pending_review
approved
expired
revoked
```

---

### Target Allowlist

The list of targets approved for project activity.

---

### Test Window

The approved time range for project activity.

---

## Report Terms

### Report

A structured output generated from project data.

Report sections may include:

* Executive summary
* Scope
* Methodology
* Campaign summary
* Findings summary
* Technical findings
* ATT&CK mapping
* Detection feedback
* Remediation plan
* Evidence appendix
* Limitations
* Cleanup status

---

### Report Builder

A module that creates report output from project data.

---

### Report Status

Allowed report status values:

```text
draft
generated
under_review
approved
final
archived
```

---

### Report Format

Supported report formats:

```text
markdown
html
pdf
docx_later
```

---

## Safety Terms

### Allowed Target

A target that is included in approved project scope.

---

### Approval-Based Workflow

A workflow where controlled, sensitive, or high-risk steps require approval before acceptance.

---

### Controlled Validation Workflow

A reviewed workflow used for authorized validation activity.

Controlled validation workflow should include:

* Approved scope
* Allowed target
* Approval reference
* Expected telemetry
* Evidence requirement
* Cleanup requirement
* Audit log

---

### Forbidden Action

An action blocked by policy.

Examples:

* Unauthorized access
* Credential theft
* Malware deployment
* Evasion tooling
* Destructive operation
* Out-of-scope activity

---

### Restricted Action

An action that requires explicit approval.

Examples:

* Safe validation workflow
* Exploit validation
* Credential exposure validation
* Persistence validation
* Lateral movement validation
* Egress telemetry validation
* External tool execution
* Production environment validation

---

### Risk Level

A classification used to control approval requirements.

Allowed values:

```text
standard
controlled
sensitive
high_risk
forbidden
```

---

### Safety Gate

A policy layer that validates scope, target allowlist, approval, restricted action, role permission, and audit requirements.

---

### Safety Model

A document and control model that defines how the framework keeps activity bound to authorized use.

---

### Scope-Bound Workflow

A workflow that references only approved targets and approved rules of engagement.

---

## Implementation Terms

### API

The interface used by clients or services to interact with RedOps Framework.

---

### JSON Schema

A structured definition used to validate example files, request bodies, and project artifacts.

---

### Object Storage

Storage for evidence files, report files, and imported files.

Examples:

* Local filesystem
* S3-compatible storage
* MinIO

---

### Project Artifact

A reviewable object created during project work.

Examples:

* Scope
* Asset
* Campaign plan
* Action log
* Evidence
* Finding
* Report
* Telemetry record
* Approval record

---

### Schema Validation

A check that confirms structured data contains required fields and valid values.

---

### Version-Aware Mapping

A mapping that stores the ATT&CK content version with the ATT&CK ID.

---

## Current Status

Current version:

```text
v0.1 Community Draft
```

Current focus:

```text
consistent terminology
project model
scope model
campaign model
evidence model
finding model
telemetry model
LLM assistance model
safety model
```
