from ..infrastructure.jwt import JWTImpl


def inject_jwt_impl_instance() -> JWTImpl:
    return JWTImpl()
