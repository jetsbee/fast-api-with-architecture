from fastapi import FastAPI

from .presentation.controllers.root_controller import router as root_router
from .presentation.controllers.auth_controller import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(root_router)
    app.include_router(auth_router)

    return app


app = create_app()
