from fastapi import APIRouter

from app.api.v1.routes import assets, attack, campaigns, health, projects, scopes

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(scopes.router, prefix="/projects/{project_id}/scopes", tags=["scopes"])
api_router.include_router(assets.router, prefix="/projects/{project_id}/assets", tags=["assets"])
api_router.include_router(campaigns.router, prefix="/projects/{project_id}/campaigns", tags=["campaigns"])
api_router.include_router(attack.router, prefix="/attack", tags=["attack"])

