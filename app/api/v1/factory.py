"""V1 FastAPI app instance declaration."""

from fastapi import FastAPI, status

from app.api.schemas.responses import ResponseErrorSchema
from app.api.v1.routers import example


INTERNAL_SERVER_ERROR: dict = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal Server Error",
        "model": ResponseErrorSchema,
    }
}


def create_app(title: str, version: str) -> FastAPI:
    api_v1 = FastAPI(
        title=title,
        version=version,
        docs_url="/",
        redoc_url=None,
        responses=INTERNAL_SERVER_ERROR,
    )

    # Добавление роутеров
    api_v1.include_router(example.router)

    return api_v1
