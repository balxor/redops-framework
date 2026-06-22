from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import SessionLocal, create_database_schema
from app.services.auth import initialize_auth_defaults


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Workflow and recordkeeping API for RedOps Framework.",
    )
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    if settings.database_auto_create:
        create_database_schema()

    with SessionLocal() as db:
        initialize_auth_defaults(db)

    return app


app = create_app()
