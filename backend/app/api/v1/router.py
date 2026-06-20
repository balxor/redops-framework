from fastapi import APIRouter
from fastapi import Depends

from app.api.v1.routes import assets, attack, auth, campaigns, health, projects, scopes
from app.core.rbac import require_roles

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projects"],
    dependencies=[Depends(require_roles("admin", "lead_operator", "operator", "reviewer"))],
)
api_router.include_router(
    scopes.router,
    prefix="/projects/{project_id}/scopes",
    tags=["scopes"],
    dependencies=[Depends(require_roles("admin", "lead_operator", "operator", "reviewer"))],
)
api_router.include_router(
    assets.router,
    prefix="/projects/{project_id}/assets",
    tags=["assets"],
    dependencies=[Depends(require_roles("admin", "lead_operator", "operator", "reviewer"))],
)
api_router.include_router(
    campaigns.router,
    prefix="/projects/{project_id}/campaigns",
    tags=["campaigns"],
    dependencies=[Depends(require_roles("admin", "lead_operator", "operator", "reviewer"))],
)
api_router.include_router(attack.router, prefix="/attack", tags=["attack"])
