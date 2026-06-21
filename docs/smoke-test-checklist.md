# Smoke Test Checklist

Status: Draft
Version: 0.1
Project: RedOps Framework

---

## Purpose

This checklist verifies the main RedOps local workflow after a frontend,
backend, migration, or CI-related change.

Use it after the stack starts cleanly and automated checks pass. The checklist
uses sanitized local development data only and must stay inside the documented
safety boundaries.

---

## Preconditions

- Backend is running and migrations are applied.
- Frontend is running and points to the backend API.
- Default local admin can log in, or a test admin account exists.
- Test data uses `example.com`, `example.test`, or RFC 5737 address ranges.
- No real client targets, secrets, credentials, or production data are used.

Recommended automated checks before manual smoke testing:

```text
backend: python -m py_compile, pytest
frontend: tsc --noEmit, vite build
```

---

## Test Data

Use values like:

| Field | Example |
| ----- | ------- |
| Project name | Example Q3 Authorized Assessment |
| Client | Example Corp |
| Scope target | app.example.test |
| Asset | app.example.test |
| Campaign | Example telemetry validation |
| Action summary | Reviewed endpoint telemetry |
| Evidence description | Sanitized alert note |
| Finding title | Example missing alert coverage |

---

## Core Workflow

### 1. Authentication

- Log in as an admin user.
- Confirm the sidebar and user context render.
- Log out and log back in.

Expected result:

- Authenticated routes load without console-visible API failures.
- Non-admin-only pages remain protected by role.

### 2. Users

- Open Users.
- Create a test operator or reviewer.
- Toggle the user between active and disabled.
- Change the user's single role with the role dropdown.

Expected result:

- User list refreshes after each mutation.
- Disabled users are marked as disabled.
- Multiple-role users are not flattened accidentally by the UI.

### 3. Project

- Create a project with sanitized metadata.
- Change project status from the project list.
- Open the project detail page.
- Change project status from Overview.

Expected result:

- Project status updates in both list and detail views.
- Recent Projects on Dashboard reflects the latest update order.

### 4. Scope And Safety

- Add a scope with one allowed target and a valid test window.
- Change scope status through the Scopes table.
- Open Safety.

Expected result:

- Approved scope count and safety summary update.
- Scope status changes are visible and audit logged.

### 5. Assets

- Add an asset inside the approved test scope.
- Change asset criticality.
- Remove a disposable asset after confirming the browser prompt.

Expected result:

- Asset list refreshes.
- Safety/audit-related views remain consistent.
- Out-of-scope assets are rejected by the backend safety gate.

### 6. Campaigns And Actions

- Create a campaign.
- Change campaign status.
- Create an action linked to the campaign or asset.
- Change action result and detection status.

Expected result:

- Status/result controls update the table.
- Action records remain notes/metadata only; no command execution path exists.

### 7. Evidence

- Add sanitized evidence metadata.
- Toggle the evidence sanitized flag.

Expected result:

- Evidence remains metadata-only unless a storage backend is intentionally added
  later.
- Unsanitized evidence is clearly marked.

### 8. Findings

- Create a finding linked to sanitized context.
- Change finding status.

Expected result:

- Finding status updates in the table.
- Severity and status badges remain readable.

### 9. Reports

- Create a report.
- Generate a report outline.
- Change report status.

Expected result:

- Report generation creates a reviewable artifact record.
- Report status updates without breaking list rendering.

### 10. Approvals

- Request an approval.
- Approve a pending approval.
- Revoke an approved approval.
- Create another approval and reject it.

Expected result:

- Approval transitions are visible.
- Restricted workflow control remains human-driven.
- Audit events are created.

### 11. LLM Drafts

- Record an LLM-assisted draft with a sanitized input summary.
- Accept the draft as a reviewer.
- Record another draft and reject it.

Expected result:

- LLM output stays review-gated.
- No LLM output directly changes project artifacts without human review.

### 12. Telemetry And Detection Gaps

- Record telemetry for a campaign, action, or finding.
- Change telemetry detection status.
- Create a detection gap.
- Change detection gap status.

Expected result:

- Telemetry and gap records stay linked to project evidence and review notes.
- Detection status values match the documented telemetry model.

### 13. ATT&CK Reference

- Open ATT&CK Techniques.
- Search by technique ID, name, tactic, platform, and source.

Expected result:

- Search filters locally.
- Empty searches show the full catalog.
- No execution or procedure automation is exposed.

### 14. Audit

- Open Audit.
- Search for recent user, project, approval, and status events.

Expected result:

- Audit search filters locally.
- Record counts show filtered and total counts where applicable.

---

## Negative Checks

Verify the following behaviors remain true:

- A non-admin cannot access Users.
- A read-only role cannot mutate project resources.
- Assets outside approved scope are rejected.
- Restricted workflows require approval rather than bypassing the approval model.
- LLM drafts require human review.
- The UI does not expose shell execution, payload generation, credential theft,
  evasion, malware, or autonomous attack execution paths.

---

## Completion Criteria

The smoke test passes when:

- The full stack starts cleanly.
- The manual workflow above completes with sanitized data.
- Typecheck and production build pass.
- Backend tests pass or any skipped tests are explicitly documented.
- GitHub Actions are green after push.
- Any failure is captured as an issue, TODO, or follow-up task with enough detail
  to reproduce.
