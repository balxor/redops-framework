from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import create_database_schema


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="API skeleton for RedOps Framework.",
    )
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    if settings.database_auto_create:
        create_database_schema()

    return app


app = create_app()
