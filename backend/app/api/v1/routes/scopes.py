from fastapi import APIRouter, HTTPException, status

from app.schemas.scope import ScopeCreate, ScopeRead, ScopeUpdate
from app.services.store import store

router = APIRouter()


@router.get("", response_model=list[ScopeRead])
def list_scopes(project_id: str) -> list[ScopeRead]:
    ensure_project(project_id)
    return store.list_scopes(project_id)


@router.post("", response_model=ScopeRead, status_code=status.HTTP_201_CREATED)
def create_scope(project_id: str, payload: ScopeCreate) -> ScopeRead:
    ensure_project(project_id)
    return store.create_scope(project_id, payload)


@router.get("/{scope_id}", response_model=ScopeRead)
def get_scope(project_id: str, scope_id: str) -> ScopeRead:
    ensure_project(project_id)
    scope = store.get_scope(project_id, scope_id)
    if scope is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scope not found")
    return scope


@router.patch("/{scope_id}", response_model=ScopeRead)
def update_scope(project_id: str, scope_id: str, payload: ScopeUpdate) -> ScopeRead:
    ensure_project(project_id)
    scope = store.update_scope(project_id, scope_id, payload)
    if scope is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scope not found")
    return scope


def ensure_project(project_id: str) -> None:
    if store.get_project(project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

