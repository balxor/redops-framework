from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.llm_task import LlmTask
from app.schemas.common import new_id, utc_now
from app.schemas.llm_task import LlmTaskCreate, LlmTaskRead, LlmTaskReview


def list_llm_tasks(db: Session, project_id: str) -> list[LlmTaskRead]:
    statement = select(LlmTask).where(LlmTask.project_id == project_id).order_by(LlmTask.created_at.desc())
    return [LlmTaskRead.model_validate(task) for task in db.scalars(statement).all()]


def create_llm_task(db: Session, project_id: str, requested_by: str, payload: LlmTaskCreate) -> LlmTaskRead:
    now = utc_now()
    task = LlmTask(
        llm_task_id=new_id("llm-task"),
        project_id=project_id,
        requested_by=requested_by,
        status="under_review",
        created_at=now,
        updated_at=now,
        **payload.model_dump(),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return LlmTaskRead.model_validate(task)


def review_llm_task(
    db: Session,
    project_id: str,
    task_id: str,
    reviewed_by: str,
    payload: LlmTaskReview,
    status_value: str,
) -> LlmTaskRead | None:
    task = db.get(LlmTask, task_id)
    if task is None or task.project_id != project_id:
        return None
    if task.status != "under_review":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only LLM drafts under review can be accepted or rejected",
        )
    now = utc_now()
    task.status = status_value
    task.reviewed_by = reviewed_by
    task.review_note = payload.review_note
    task.reviewed_at = now
    task.updated_at = now
    db.commit()
    db.refresh(task)
    return LlmTaskRead.model_validate(task)
