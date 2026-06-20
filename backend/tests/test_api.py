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
