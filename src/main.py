from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader

from . import middleware as custom_middleware
from .error import add_custom_exception_handlers
from .routing import router, activation as routes_activation


def create_app() -> FastAPI:
    # Easy auth in swagger ui
    authorization_header_scheme = APIKeyHeader(name="Authorization", auto_error=False)

    app = FastAPI(dependencies=[Depends(authorization_header_scheme)])

    add_custom_exception_handlers(app)

    # Order of adding middleware matters. (the last one is invoked first and returns the last)
    app.add_middleware(middleware_class=custom_middleware.UnexpectedErrorMiddleware)

    routes_activation.connect_components()
    app.include_router(router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
