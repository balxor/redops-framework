from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.evidence import EvidenceCreate, EvidenceRead, EvidenceUpdate
from app.schemas.user import CurrentUser
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[EvidenceRead])
def list_evidence(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[EvidenceRead]:
    ensure_project_access(db, current_user, project_id)
    return store.list_evidence(db, project_id)


@router.post("", response_model=EvidenceRead, status_code=status.HTTP_201_CREATED)
def create_evidence(
    project_id: str,
    payload: EvidenceCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> EvidenceRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    return store.create_evidence(db, project_id, current_user.user_id, payload)


@router.get("/{evidence_id}", response_model=EvidenceRead)
def get_evidence(
    project_id: str,
    evidence_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> EvidenceRead:
    ensure_project_access(db, current_user, project_id)
    evidence = store.get_evidence(db, project_id, evidence_id)
    if evidence is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence not found")
    return evidence


@router.patch("/{evidence_id}", response_model=EvidenceRead)
def update_evidence(
    project_id: str,
    evidence_id: str,
    payload: EvidenceUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> EvidenceRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    evidence = store.update_evidence(db, project_id, evidence_id, payload)
    if evidence is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence not found")
    return evidence

