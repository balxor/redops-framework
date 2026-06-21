from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import create_app


client = TestClient(create_app())


def auth_headers() -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "admin-change-me"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def login_headers(email: str, password: str) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_project_with_approved_scope(headers: dict[str, str], name: str, target: str) -> str:
    project_response = client.post(
        "/api/v1/projects",
        headers=headers,
        json={
            "name": name,
            "engagement_type": "internal_pentest",
            "status": "draft",
        },
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["project_id"]

    scope_response = client.post(
        f"/api/v1/projects/{project_id}/scopes",
        headers=headers,
        json={
            "status": "approved",
            "allowed_targets": [
                {
                    "type": "domain",
                    "value": target,
                    "environment": "lab",
                }
            ],
            "forbidden_targets": [],
            "test_window": {
                "start": "2026-06-20T00:00:00Z",
                "end": "2026-06-30T00:00:00Z",
                "timezone": "Asia/Jakarta",
            },
            "approval_required": True,
        },
    )
    assert scope_response.status_code == 201
    return project_id


def test_health_check() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_auth_me() -> None:
    response = client.get("/api/v1/auth/me", headers=auth_headers())

    assert response.status_code == 200
    assert response.json()["roles"] == ["admin"]


def test_admin_user_management_flow() -> None:
    headers = auth_headers()
    email = f"operator-{uuid4().hex[:8]}@example.com"
    create_response = client.post(
        "/api/v1/users",
        headers=headers,
        json={
            "email": email,
            "full_name": "Operator Example",
            "password": "operator-change-me",
            "roles": ["operator"],
            "is_active": True,
        },
    )

    assert create_response.status_code == 201
    user = create_response.json()
    assert user["roles"] == ["operator"]

    patch_response = client.patch(
        f"/api/v1/users/{user['user_id']}",
        headers=headers,
        json={"roles": ["operator", "reviewer"], "full_name": "Operator Reviewer"},
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["roles"] == ["operator", "reviewer"]


def test_project_membership_access_flow() -> None:
    admin_headers = auth_headers()
    email = f"member-{uuid4().hex[:8]}@example.com"
    password = "member-change-me"
    user_response = client.post(
        "/api/v1/users",
        headers=admin_headers,
        json={
            "email": email,
            "full_name": "Member Example",
            "password": password,
            "roles": ["operator"],
            "is_active": True,
        },
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["user_id"]

    project_response = client.post(
        "/api/v1/projects",
        headers=admin_headers,
        json={
            "name": "Membership Access Assessment",
            "engagement_type": "internal_pentest",
            "status": "draft",
        },
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["project_id"]

    member_response = client.post(
        f"/api/v1/projects/{project_id}/members",
        headers=admin_headers,
        json={"user_id": user_id, "project_role": "operator"},
    )
    assert member_response.status_code == 201

    member_headers = login_headers(email, password)
    get_response = client.get(f"/api/v1/projects/{project_id}", headers=member_headers)
    assert get_response.status_code == 200
    assert get_response.json()["project_id"] == project_id

    list_response = client.get("/api/v1/projects", headers=member_headers)
    assert list_response.status_code == 200
    assert [project["project_id"] for project in list_response.json()] == [project_id]


def test_project_asset_campaign_flow() -> None:
    headers = auth_headers()
    project_response = client.post(
        "/api/v1/projects",
        headers=headers,
        json={
            "name": "Example Red Team Assessment",
            "engagement_type": "red_team",
            "status": "draft",
            "client_name": "Example Client",
        },
    )

    assert project_response.status_code == 201
    project = project_response.json()
    project_id = project["project_id"]

    scope_response = client.post(
        f"/api/v1/projects/{project_id}/scopes",
        headers=headers,
        json={
            "status": "approved",
            "allowed_targets": [
                {
                    "type": "domain",
                    "value": "app.example.test",
                    "environment": "lab",
                }
            ],
            "forbidden_targets": [
                {
                    "type": "domain",
                    "value": "forbidden.example.test",
                    "environment": "lab",
                }
            ],
            "test_window": {
                "start": "2026-06-20T00:00:00Z",
                "end": "2026-06-30T00:00:00Z",
                "timezone": "Asia/Jakarta",
            },
            "approval_required": True,
        },
    )
    assert scope_response.status_code == 201

    safety_response = client.get(f"/api/v1/projects/{project_id}/safety/summary", headers=headers)
    assert safety_response.status_code == 200
    assert safety_response.json()["has_approved_scope"] is True

    asset_response = client.post(
        f"/api/v1/projects/{project_id}/assets",
        headers=headers,
        json={
            "value": "app.example.test",
            "type": "domain",
            "environment": "lab",
            "criticality": "medium",
        },
    )

    assert asset_response.status_code == 201
    assert asset_response.json()["project_id"] == project_id

    campaign_response = client.post(
        f"/api/v1/projects/{project_id}/campaigns",
        headers=headers,
        json={
            "name": "Discovery Validation",
            "objective": "Validate controlled discovery workflow.",
            "status": "planned",
            "steps": [
                {
                    "title": "Review network service discovery telemetry",
                    "attack_technique_id": "T1046",
                    "status": "planned",
                    "approval_required": True,
                }
            ],
        },
    )

    assert campaign_response.status_code == 201
    assert campaign_response.json()["steps"][0]["attack_technique_id"] == "T1046"

    action_response = client.post(
        f"/api/v1/projects/{project_id}/actions",
        headers=headers,
        json={
            "campaign_id": campaign_response.json()["campaign_id"],
            "asset_id": asset_response.json()["asset_id"],
            "action_type": "detection_validation_note",
            "action_summary": "Reviewed endpoint telemetry for discovery activity.",
            "action_detail": "Telemetry review was performed against approved lab scope.",
            "result": "executed",
            "detection_status": "partially_detected",
        },
    )

    assert action_response.status_code == 201
    assert action_response.json()["operator_id"].startswith("user-")

    evidence_response = client.post(
        f"/api/v1/projects/{project_id}/evidence",
        headers=headers,
        json={
            "action_id": action_response.json()["action_id"],
            "asset_id": asset_response.json()["asset_id"],
            "evidence_type": "edr_alert",
            "file_name": "endpoint-event-review.txt",
            "file_size": 128,
            "mime_type": "text/plain",
            "file_hash_sha256": "a" * 64,
            "description": "Sanitized endpoint alert reference for discovery validation.",
            "sanitized": True,
        },
    )

    assert evidence_response.status_code == 201
    assert evidence_response.json()["action_id"] == action_response.json()["action_id"]

    telemetry_response = client.post(
        f"/api/v1/projects/{project_id}/telemetry",
        headers=headers,
        json={
            "action_id": action_response.json()["action_id"],
            "asset_id": asset_response.json()["asset_id"],
            "evidence_id": evidence_response.json()["evidence_id"],
            "attack_technique_id": "T1046",
            "expected_telemetry": [
                {
                    "name": "network service discovery alert",
                    "data_source": "edr",
                    "signal": "service discovery activity",
                    "required": True,
                }
            ],
            "observed_telemetry": [
                {
                    "name": "partial endpoint alert",
                    "data_source": "edr",
                    "signal": "endpoint alert without full command context",
                    "required": False,
                }
            ],
            "data_source": "edr",
            "detection_status": "partially_detected",
            "review_note": "Command context was incomplete in reviewed telemetry.",
        },
    )
    assert telemetry_response.status_code == 201
    telemetry = telemetry_response.json()
    assert telemetry["detection_status"] == "partially_detected"
    assert telemetry["evidence_id"] == evidence_response.json()["evidence_id"]

    gap_response = client.post(
        f"/api/v1/projects/{project_id}/detection-gaps",
        headers=headers,
        json={
            "telemetry_id": telemetry["telemetry_id"],
            "evidence_id": evidence_response.json()["evidence_id"],
            "asset_id": asset_response.json()["asset_id"],
            "attack_technique_id": "T1046",
            "gap_type": "incomplete_telemetry",
            "summary": "Command context was incomplete in reviewed endpoint telemetry.",
            "impact": "Investigation context may be incomplete.",
            "recommendation": "Review endpoint telemetry collection and parsing.",
        },
    )
    assert gap_response.status_code == 201
    assert gap_response.json()["telemetry_id"] == telemetry["telemetry_id"]

    finding_response = client.post(
        f"/api/v1/projects/{project_id}/findings",
        headers=headers,
        json={
            "title": "Endpoint discovery activity was partially detected",
            "summary": "Discovery validation produced partial endpoint telemetry.",
            "severity": "medium",
            "status": "draft",
            "affected_assets": [asset_response.json()["asset_id"]],
            "attack_technique_id": "T1046",
            "attack_mapping": [{"technique_id": "T1046", "tactic": "discovery"}],
            "evidence_ids": [evidence_response.json()["evidence_id"]],
            "impact": "Detection coverage requires tuning.",
            "likelihood": "medium",
            "recommendation": "Review endpoint detection rule coverage for discovery activity.",
        },
    )

    assert finding_response.status_code == 201
    assert finding_response.json()["evidence_ids"] == [evidence_response.json()["evidence_id"]]

    patch_finding_response = client.patch(
        f"/api/v1/projects/{project_id}/findings/{finding_response.json()['finding_id']}",
        headers=headers,
        json={"status": "under_review"},
    )
    assert patch_finding_response.status_code == 200
    assert patch_finding_response.json()["status"] == "under_review"

    report_response = client.post(
        f"/api/v1/projects/{project_id}/reports",
        headers=headers,
        json={
            "title": "Example Red Team Assessment Report",
            "version": "0.1",
            "status": "draft",
            "format": "markdown",
            "finding_ids": [finding_response.json()["finding_id"]],
            "evidence_ids": [evidence_response.json()["evidence_id"]],
            "sections": [
                {
                    "key": "executive_summary",
                    "title": "Executive Summary",
                    "content": "Draft summary for reviewed findings.",
                    "order": 1,
                }
            ],
        },
    )
    assert report_response.status_code == 201
    assert report_response.json()["finding_ids"] == [finding_response.json()["finding_id"]]

    generated_report_response = client.post(
        f"/api/v1/projects/{project_id}/reports/generate",
        headers=headers,
        json={
            "title": "Generated Project Outline",
            "format": "markdown",
            "include_sections": ["executive_summary", "findings_summary", "evidence_appendix"],
        },
    )
    assert generated_report_response.status_code == 201
    generated_report = generated_report_response.json()
    assert generated_report["status"] == "generated"
    assert generated_report["generated_by"].startswith("user-")
    assert [section["key"] for section in generated_report["sections"]] == [
        "executive_summary",
        "findings_summary",
        "evidence_appendix",
    ]
    assert generated_report["finding_ids"] == [finding_response.json()["finding_id"]]
    assert generated_report["evidence_ids"] == [evidence_response.json()["evidence_id"]]

    patch_report_response = client.patch(
        f"/api/v1/projects/{project_id}/reports/{report_response.json()['report_id']}",
        headers=headers,
        json={"status": "under_review"},
    )
    assert patch_report_response.status_code == 200
    assert patch_report_response.json()["status"] == "under_review"

    list_evidence_response = client.get(f"/api/v1/projects/{project_id}/evidence", headers=headers)
    assert list_evidence_response.status_code == 200
    assert len(list_evidence_response.json()) == 1

    list_actions_response = client.get(f"/api/v1/projects/{project_id}/actions", headers=headers)
    assert list_actions_response.status_code == 200
    assert len(list_actions_response.json()) == 1

    audit_response = client.get(f"/api/v1/projects/{project_id}/audit", headers=headers)
    assert audit_response.status_code == 200
    audit_actions = {event["action"] for event in audit_response.json()}
    assert {
        "project.created",
        "scope.created",
        "asset.created",
        "campaign.created",
        "action.created",
        "evidence.created",
        "telemetry.created",
        "detection_gap.created",
        "finding.created",
        "finding.updated",
        "report.created",
        "report.generated",
        "report.updated",
    }.issubset(audit_actions)


def test_safety_gate_rejects_out_of_scope_asset() -> None:
    headers = auth_headers()
    project_response = client.post(
        "/api/v1/projects",
        headers=headers,
        json={
            "name": "Out of Scope Assessment",
            "engagement_type": "internal_pentest",
            "status": "draft",
        },
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["project_id"]

    scope_response = client.post(
        f"/api/v1/projects/{project_id}/scopes",
        headers=headers,
        json={
            "status": "approved",
            "allowed_targets": [
                {
                    "type": "domain",
                    "value": "allowed.example.test",
                    "environment": "lab",
                }
            ],
            "forbidden_targets": [],
            "test_window": {
                "start": "2026-06-20T00:00:00Z",
                "end": "2026-06-30T00:00:00Z",
                "timezone": "Asia/Jakarta",
            },
            "approval_required": True,
        },
    )
    assert scope_response.status_code == 201

    asset_response = client.post(
        f"/api/v1/projects/{project_id}/assets",
        headers=headers,
        json={
            "value": "outside.example.test",
            "type": "domain",
            "environment": "lab",
            "criticality": "medium",
        },
    )

    assert asset_response.status_code == 403
    assert asset_response.json()["detail"] == "Asset target is outside approved scope"


def test_rejects_cross_project_references() -> None:
    headers = auth_headers()
    source_project_id = create_project_with_approved_scope(
        headers,
        "Reference Source Assessment",
        "source.example.test",
    )
    target_project_id = create_project_with_approved_scope(
        headers,
        "Reference Target Assessment",
        "target.example.test",
    )

    source_asset_response = client.post(
        f"/api/v1/projects/{source_project_id}/assets",
        headers=headers,
        json={
            "value": "source.example.test",
            "type": "domain",
            "environment": "lab",
            "criticality": "medium",
        },
    )
    assert source_asset_response.status_code == 201
    source_asset_id = source_asset_response.json()["asset_id"]

    source_finding_response = client.post(
        f"/api/v1/projects/{source_project_id}/findings",
        headers=headers,
        json={
            "title": "Source project finding",
            "summary": "Finding kept in the source project.",
            "severity": "low",
            "status": "draft",
            "affected_assets": [source_asset_id],
        },
    )
    assert source_finding_response.status_code == 201
    source_finding_id = source_finding_response.json()["finding_id"]

    finding_response = client.post(
        f"/api/v1/projects/{target_project_id}/findings",
        headers=headers,
        json={
            "title": "Invalid target finding",
            "summary": "This finding tries to reference an asset from another project.",
            "severity": "medium",
            "status": "draft",
            "affected_assets": [source_asset_id],
        },
    )
    assert finding_response.status_code == 400
    assert finding_response.json()["detail"] == "Asset reference is invalid for this project"

    report_response = client.post(
        f"/api/v1/projects/{target_project_id}/reports",
        headers=headers,
        json={
            "title": "Invalid target report",
            "version": "0.1",
            "status": "draft",
            "format": "markdown",
            "finding_ids": [source_finding_id],
        },
    )
    assert report_response.status_code == 400
    assert report_response.json()["detail"] == "Finding reference is invalid for this project"


def test_restricted_action_requires_approval() -> None:
    headers = auth_headers()
    project_id = create_project_with_approved_scope(
        headers,
        "Restricted Action Assessment",
        "restricted.example.test",
    )

    restricted_scope_response = client.post(
        f"/api/v1/projects/{project_id}/scopes",
        headers=headers,
        json={
            "status": "approved",
            "allowed_targets": [
                {
                    "type": "domain",
                    "value": "restricted.example.test",
                    "environment": "lab",
                }
            ],
            "forbidden_targets": [],
            "restricted_actions": ["exploit_validation"],
            "test_window": {
                "start": "2026-06-20T00:00:00Z",
                "end": "2026-06-30T00:00:00Z",
                "timezone": "Asia/Jakarta",
            },
            "approval_required": True,
        },
    )
    assert restricted_scope_response.status_code == 201

    blocked_response = client.post(
        f"/api/v1/projects/{project_id}/actions",
        headers=headers,
        json={
            "action_type": "exploit_validation_note",
            "action_summary": "Document controlled exploit validation review.",
            "result": "planned",
            "detection_status": "unknown",
        },
    )
    assert blocked_response.status_code == 409
    assert "Approved action_type approval is required" in blocked_response.json()["detail"]

    approval_response = client.post(
        f"/api/v1/projects/{project_id}/approvals",
        headers=headers,
        json={
            "entity_type": "action_type",
            "entity_id": "exploit_validation_note",
            "risk_level": "sensitive",
            "reason": "Controlled validation note is required for authorized lab review.",
        },
    )
    assert approval_response.status_code == 201
    approval_id = approval_response.json()["approval_id"]

    approve_response = client.post(
        f"/api/v1/projects/{project_id}/approvals/{approval_id}/approve",
        headers=headers,
        json={"decision_note": "Approved for lab-only documentation workflow."},
    )
    assert approve_response.status_code == 200
    assert approve_response.json()["status"] == "approved"

    allowed_response = client.post(
        f"/api/v1/projects/{project_id}/actions",
        headers=headers,
        json={
            "action_type": "exploit_validation_note",
            "action_summary": "Document controlled exploit validation review.",
            "result": "planned",
            "detection_status": "unknown",
        },
    )
    assert allowed_response.status_code == 201

    audit_response = client.get(f"/api/v1/projects/{project_id}/audit", headers=headers)
    assert audit_response.status_code == 200
    audit_actions = {event["action"] for event in audit_response.json()}
    assert {"approval.requested", "approval.approved", "action.created"}.issubset(audit_actions)


def test_llm_draft_requires_human_review() -> None:
    headers = auth_headers()
    project_id = create_project_with_approved_scope(
        headers,
        "LLM Draft Review Assessment",
        "llm-review.example.test",
    )

    create_response = client.post(
        f"/api/v1/projects/{project_id}/llm/tasks",
        headers=headers,
        json={
            "task_type": "finding_draft",
            "entity_type": "finding",
            "entity_id": "draft-finding",
            "input_summary": "Draft a reviewed finding summary from sanitized notes.",
            "output_content": "Draft finding text requiring reviewer validation before use.",
            "assumptions": ["Scope is approved."],
            "limitations": ["Draft content is not a confirmed finding."],
            "requires_review": True,
        },
    )
    assert create_response.status_code == 201
    task = create_response.json()
    assert task["status"] == "under_review"
    assert task["reviewed_by"] is None

    accept_response = client.post(
        f"/api/v1/projects/{project_id}/llm/tasks/{task['llm_task_id']}/accept",
        headers=headers,
        json={"review_note": "Reviewed and accepted as draft language only."},
    )
    assert accept_response.status_code == 200
    accepted = accept_response.json()
    assert accepted["status"] == "accepted"
    assert accepted["reviewed_by"].startswith("user-")

    second_accept_response = client.post(
        f"/api/v1/projects/{project_id}/llm/tasks/{task['llm_task_id']}/accept",
        headers=headers,
        json={"review_note": "Second accept should fail."},
    )
    assert second_accept_response.status_code == 409

    audit_response = client.get(f"/api/v1/projects/{project_id}/audit", headers=headers)
    assert audit_response.status_code == 200
    audit_actions = {event["action"] for event in audit_response.json()}
    assert {"llm.output.generated", "llm.output.accepted"}.issubset(audit_actions)
