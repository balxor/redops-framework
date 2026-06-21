from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.report import ReportCreate, ReportGenerateRequest, ReportRead, ReportUpdate
from app.schemas.user import CurrentUser
from app.services.audit import record_audit_event
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access
from app.services.report_builder import build_report_outline
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[ReportRead])
def list_reports(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[ReportRead]:
    ensure_project_access(db, current_user, project_id)
    return store.list_reports(db, project_id)


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def create_report(
    project_id: str,
    payload: ReportCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ReportRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    report = store.create_report(db, project_id, payload)
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="report.created",
        resource_type="report",
        resource_id=report.report_id,
        summary=f"Report created: {report.title}",
    )
    return report


@router.post("/generate", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def generate_report(
    project_id: str,
    payload: ReportGenerateRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ReportRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    report_payload = build_report_outline(db, project_id, current_user.user_id, payload)
    report = store.create_report(db, project_id, report_payload)
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="report.generated",
        resource_type="report",
        resource_id=report.report_id,
        summary=f"Report outline generated: {report.title}",
    )
    return report


@router.get("/{report_id}", response_model=ReportRead)
def get_report(
    project_id: str,
    report_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ReportRead:
    ensure_project_access(db, current_user, project_id)
    report = store.get_report(db, project_id, report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


@router.patch("/{report_id}", response_model=ReportRead)
def update_report(
    project_id: str,
    report_id: str,
    payload: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> ReportRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"reviewer"})
    report = store.update_report(db, project_id, report_id, payload)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="report.updated",
        resource_type="report",
        resource_id=report_id,
        summary=f"Report updated: {report.title}",
    )
    return report
