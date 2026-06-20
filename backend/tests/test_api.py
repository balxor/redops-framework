from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_health_check() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_project_asset_campaign_flow() -> None:
    project_response = client.post(
        "/api/v1/projects",
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

    asset_response = client.post(
        f"/api/v1/projects/{project_id}/assets",
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

