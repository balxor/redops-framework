from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_user
from app.schemas.llm_task import LlmTaskCreate, LlmTaskRead, LlmTaskReview
from app.schemas.user import CurrentUser
from app.services.audit import record_audit_event
from app.services.llm_tasks import create_llm_task, list_llm_tasks, review_llm_task
from app.services.memberships import PROJECT_WRITE_ROLES, ensure_project_access

router = APIRouter()


@router.get("/tasks", response_model=list[LlmTaskRead])
def get_llm_tasks(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[LlmTaskRead]:
    ensure_project_access(db, current_user, project_id)
    return list_llm_tasks(db, project_id)


@router.post("/tasks", response_model=LlmTaskRead, status_code=status.HTTP_201_CREATED)
def post_llm_task(
    project_id: str,
    payload: LlmTaskCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> LlmTaskRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"operator"})
    task = create_llm_task(db, project_id, current_user.user_id, payload)
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="llm.output.generated",
        resource_type="llm_task",
        resource_id=task.llm_task_id,
        summary=f"LLM-assisted draft recorded: {task.task_type}",
    )
    return task


@router.post("/tasks/{task_id}/accept", response_model=LlmTaskRead)
def accept_llm_task(
    project_id: str,
    task_id: str,
    payload: LlmTaskReview,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> LlmTaskRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"reviewer"})
    task = review_llm_task(db, project_id, task_id, current_user.user_id, payload, "accepted")
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LLM task not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="llm.output.accepted",
        resource_type="llm_task",
        resource_id=task_id,
        summary=f"LLM-assisted draft accepted: {task.task_type}",
    )
    return task


@router.post("/tasks/{task_id}/reject", response_model=LlmTaskRead)
def reject_llm_task(
    project_id: str,
    task_id: str,
    payload: LlmTaskReview,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> LlmTaskRead:
    ensure_project_access(db, current_user, project_id, PROJECT_WRITE_ROLES | {"reviewer"})
    task = review_llm_task(db, project_id, task_id, current_user.user_id, payload, "rejected")
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LLM task not found")
    record_audit_event(
        db,
        project_id=project_id,
        actor_user_id=current_user.user_id,
        action="llm.output.rejected",
        resource_type="llm_task",
        resource_id=task_id,
        summary=f"LLM-assisted draft rejected: {task.task_type}",
    )
    return task
