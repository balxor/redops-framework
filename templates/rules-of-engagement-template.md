# Rules of Engagement Template

Status: Draft

## Engagement Summary

| Field | Value |
| ----- | ----- |
| Project name |  |
| Client or owner |  |
| Engagement type |  |
| Start date |  |
| End date |  |
| Primary contact |  |
| Emergency contact |  |

## Authorized Scope

List only approved targets.

| Target | Type | Environment | Notes |
| ------ | ---- | ----------- | ----- |
| example.com | domain | test | Sanitized example |

## Explicitly Excluded Targets

| Target | Reason |
| ------ | ------ |
| production-payment.example.com | Not approved for testing |

## Test Window

| Window | Date | Start | End | Time zone |
| ------ | ---- | ----- | --- | --------- |
| Primary |  |  |  |  |

## Allowed Activities

* Reconnaissance against approved targets
* Manual validation within approved scope
* Evidence collection using sanitized data
* Detection and telemetry review

## Restricted Activities

Restricted activities require written approval before execution.

* High-volume scanning
* Credential testing
* Service-impacting validation
* External tool imports

## Prohibited Activities

* Testing outside approved scope
* Destructive actions
* Persistence, evasion, or malware deployment
* Exfiltration of real sensitive data
* Public disclosure without approval

## Evidence Requirements

Evidence must be sanitized before sharing publicly.

| Evidence type | Required metadata |
| ------------- | ----------------- |
| Screenshot | Timestamp, target, description |
| Log excerpt | Timestamp, source, redaction note |
| Finding reference | Finding ID, affected asset |

## Approval Record

| Approval | Approver | Date | Notes |
| -------- | -------- | ---- | ----- |
| Scope approval |  |  |  |
| Restricted action approval |  |  |  |

## Cleanup Requirements

Document cleanup tasks and owner.

| Task | Owner | Due date | Status |
| ---- | ----- | -------- | ------ |
| Remove test data |  |  | planned |

## Sign-Off

| Role | Name | Date |
| ---- | ---- | ---- |
| Client representative |  |  |
| Lead operator |  |  |
| Reviewer |  |  |
