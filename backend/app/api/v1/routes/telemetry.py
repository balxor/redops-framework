from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.telemetry import (
    DetectionGapCreate,
    DetectionGapRead,
    DetectionGapUpdate,
    TelemetryCreate,
    TelemetryRead,
    TelemetryUpdate,
)
from app.schemas.user import CurrentUser
from app.services.audit import record_audit_event
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access
from app.services.telemetry import (
    create_detection_gap,
    create_telemetry,
    list_detection_gaps,
    list_telemetry,
    update_detection_gap,
    update_telemetry,
)

router = APIRouter()


@router.get("/telemetry", response_model=list[TelemetryRead])
def get_telemetry(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[TelemetryRead]:
    ensure_project_access(db, current_user, project_id)
    return list_telemetry(db, project_id)


@router.post("/telemetry", response_model=TelemetryRead, status_code=status.HTTP_201_CREATED)
def post_telemetry(
    project_id: str,
    payload: TelemetryCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> TelemetryRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator", "reviewer"})
    telemetry = create_telemetry(db, project_id, payload)
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="telemetry.created",
        resource_type="telemetry",
        resource_id=telemetry.telemetry_id,
        summary=f"Telemetry recorded with status {telemetry.detection_status}",
    )
    return telemetry


@router.patch("/telemetry/{telemetry_id}", response_model=TelemetryRead)
def patch_telemetry(
    project_id: str,
    telemetry_id: str,
    payload: TelemetryUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> TelemetryRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"reviewer"})
    telemetry = update_telemetry(db, project_id, telemetry_id, payload)
    if telemetry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Telemetry not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="telemetry.updated",
        resource_type="telemetry",
        resource_id=telemetry_id,
        summary=f"Telemetry updated with status {telemetry.detection_status}",
    )
    return telemetry


@router.get("/detection-gaps", response_model=list[DetectionGapRead])
def get_detection_gaps(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[DetectionGapRead]:
    ensure_project_access(db, current_user, project_id)
    return list_detection_gaps(db, project_id)


@router.post("/detection-gaps", response_model=DetectionGapRead, status_code=status.HTTP_201_CREATED)
def post_detection_gap(
    project_id: str,
    payload: DetectionGapCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> DetectionGapRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator", "reviewer"})
    gap = create_detection_gap(db, project_id, current_user.user_id, payload)
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="detection_gap.created",
        resource_type="detection_gap",
        resource_id=gap.gap_id,
        summary=f"Detection gap created: {gap.summary[:120]}",
    )
    return gap


@router.patch("/detection-gaps/{gap_id}", response_model=DetectionGapRead)
def patch_detection_gap(
    project_id: str,
    gap_id: str,
    payload: DetectionGapUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> DetectionGapRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"reviewer"})
    gap = update_detection_gap(db, project_id, gap_id, payload)
    if gap is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detection gap not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="detection_gap.updated",
        resource_type="detection_gap",
        resource_id=gap_id,
        summary=f"Detection gap updated: {gap.summary[:120]}",
    )
    return gap
