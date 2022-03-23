from ..domain.models.jwt import JWTModel


class JWTImpl(JWTModel):
    @classmethod
    def create(cls, username):
        super().create(username)  # Confirm parent's signiture

        jwt_string = f"{username}!@#$1234"
        expires_in = 20220314
        return (jwt_string, expires_in)

    @classmethod
    def revoke(cls):
        pass

    @classmethod
    def verify(cls):
        pass

    @classmethod
    def renew(cls):
        pass
