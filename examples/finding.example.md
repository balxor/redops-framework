# Example Finding

Status: Draft

## Summary

| Field | Value |
| ----- | ----- |
| Finding ID | finding-001 |
| Project ID | example-project |
| Title | Missing Security Header on Test Application |
| Severity | Low |
| Affected asset | app.example.com |
| ATT&CK technique | T1592 |

## Description

The approved test application response did not include one expected browser
security header during authorized review.

## Evidence

| Evidence ID | Type | Description |
| ----------- | ---- | ----------- |
| evidence-001 | sanitized_log_excerpt | Header review output with sensitive values removed |

## Impact

The missing header may reduce browser-side hardening. No exploit attempt was
performed as part of this example.

## Recommendation

Review application security header configuration and apply the organization's
approved baseline.

## Detection Feedback

| Data source | Detection status | Notes |
| ----------- | ---------------- | ----- |
| Web server logs | detected | Authorized request was visible in logs |
