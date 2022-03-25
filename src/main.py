from fastapi import FastAPI

from .presentation.controllers.root_controller import router as root_router
from .presentation.controllers.auth_controller import router as auth_router
from .errors.handlers import add_custom_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(root_router)
    app.include_router(auth_router)

    add_custom_exception_handlers(app)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
