from fastapi import APIRouter, HTTPException, status

from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[ProjectRead])
def list_projects() -> list[ProjectRead]:
    return store.list_projects()


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate) -> ProjectRead:
    return store.create_project(payload)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: str) -> ProjectRead:
    project = store.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(project_id: str, payload: ProjectUpdate) -> ProjectRead:
    project = store.update_project(project_id, payload)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str) -> None:
    deleted = store.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

