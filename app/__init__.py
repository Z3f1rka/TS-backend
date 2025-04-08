from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import object_router
from app.api import user_router
from app.core import settings


# TODO: настроить нормально CORS
def create_app() -> FastAPI:
    app = FastAPI(swagger_ui_parameters={
        "url": f"http://{settings.API_HOST}:{settings.API_PORT}{settings.PREFIX}/openapi.json"})
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(user_router)
    app.include_router(object_router)
    return app
