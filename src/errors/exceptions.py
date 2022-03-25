class UserAlreadyExistenceException(Exception):
    def __init__(self, name: str):
        self.name = name
        self.detail = "User already exists."
        # To use parent's __str__()
        super().__init__({"name": self.name, "detail": self.detail})
