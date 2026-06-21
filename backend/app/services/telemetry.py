from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.action import Action
from app.models.asset import Asset
from app.models.campaign import Campaign
from app.models.detection_gap import DetectionGap
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.telemetry import Telemetry
from app.schemas.common import new_id, utc_now
from app.schemas.telemetry import (
    DetectionGapCreate,
    DetectionGapRead,
    DetectionGapUpdate,
    TelemetryCreate,
    TelemetryRead,
    TelemetryUpdate,
)


def list_telemetry(db: Session, project_id: str) -> list[TelemetryRead]:
    statement = select(Telemetry).where(Telemetry.project_id == project_id).order_by(Telemetry.created_at.desc())
    return [TelemetryRead.model_validate(item) for item in db.scalars(statement).all()]


def create_telemetry(db: Session, project_id: str, payload: TelemetryCreate) -> TelemetryRead:
    _validate_refs(db, project_id, payload.model_dump(mode="json"))
    now = utc_now()
    telemetry = Telemetry(
        telemetry_id=new_id("telemetry"),
        project_id=project_id,
        created_at=now,
        updated_at=now,
        **payload.model_dump(),
    )
    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)
    return TelemetryRead.model_validate(telemetry)


def update_telemetry(db: Session, project_id: str, telemetry_id: str, payload: TelemetryUpdate) -> TelemetryRead | None:
    telemetry = db.get(Telemetry, telemetry_id)
    if telemetry is None or telemetry.project_id != project_id:
        return None
    _validate_refs(db, project_id, payload.model_dump(mode="json", exclude_unset=True))
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(telemetry, key, value)
    telemetry.updated_at = utc_now()
    db.commit()
    db.refresh(telemetry)
    return TelemetryRead.model_validate(telemetry)


def list_detection_gaps(db: Session, project_id: str) -> list[DetectionGapRead]:
    statement = select(DetectionGap).where(DetectionGap.project_id == project_id).order_by(DetectionGap.created_at.desc())
    return [DetectionGapRead.model_validate(item) for item in db.scalars(statement).all()]


def create_detection_gap(
    db: Session,
    project_id: str,
    created_by: str,
    payload: DetectionGapCreate,
) -> DetectionGapRead:
    _validate_refs(db, project_id, payload.model_dump(mode="json"))
    now = utc_now()
    gap = DetectionGap(
        gap_id=new_id("gap"),
        project_id=project_id,
        created_by=created_by,
        created_at=now,
        updated_at=now,
        **payload.model_dump(mode="json"),
    )
    db.add(gap)
    db.commit()
    db.refresh(gap)
    return DetectionGapRead.model_validate(gap)


def update_detection_gap(
    db: Session,
    project_id: str,
    gap_id: str,
    payload: DetectionGapUpdate,
) -> DetectionGapRead | None:
    gap = db.get(DetectionGap, gap_id)
    if gap is None or gap.project_id != project_id:
        return None
    data = payload.model_dump(mode="json", exclude_unset=True)
    _validate_refs(db, project_id, data)
    for key, value in data.items():
        setattr(gap, key, value)
    gap.updated_at = utc_now()
    db.commit()
    db.refresh(gap)
    return DetectionGapRead.model_validate(gap)


def _validate_refs(db: Session, project_id: str, data: dict) -> None:
    _ensure_project_ref(db, Campaign, data.get("campaign_id"), project_id, "Campaign")
    _ensure_project_ref(db, Action, data.get("action_id"), project_id, "Action")
    _ensure_project_ref(db, Asset, data.get("asset_id"), project_id, "Asset")
    _ensure_project_ref(db, Evidence, data.get("evidence_id"), project_id, "Evidence")
    _ensure_project_ref(db, Finding, data.get("finding_id"), project_id, "Finding")
    _ensure_project_ref(db, Telemetry, data.get("telemetry_id"), project_id, "Telemetry")


def _ensure_project_ref(db: Session, model: type, entity_id: str | None, project_id: str, label: str) -> None:
    if entity_id is None:
        return
    entity = db.get(model, entity_id)
    if entity is None or getattr(entity, "project_id", None) != project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{label} reference is invalid for this project",
        )
