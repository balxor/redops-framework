# Example Report Outline

Status: Draft

## Executive Summary

Summarize the authorized assessment, approved scope, and overall risk.

## Scope

| Target | Type | Status |
| ------ | ---- | ------ |
| app.example.com | domain | approved |

## Findings

| Finding ID | Title | Severity |
| ---------- | ----- | -------- |
| finding-001 | Missing Security Header on Test Application | Low |

## ATT&CK Mapping

| Technique ID | Technique name | Finding ID |
| ------------ | -------------- | ---------- |
| T1592 | Gather Victim Host Information | finding-001 |

## Detection Feedback

| Activity | Detection status | Evidence |
| -------- | ---------------- | -------- |
| Header review request | detected | evidence-001 |

## Limitations

* This is a sanitized documentation example.
* No destructive validation is included.
