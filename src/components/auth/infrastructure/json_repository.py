import json

from typing import Dict, Optional

from ..domain.repositories.user import UserRepository
from ..domain.models.user import UserModel


class JsonRepository:
    def __init__(self, db_loc: str) -> None:
        self._db_loc = db_loc
        self._db = self.__connect_database()

    def __connect_database(self) -> Dict:
        with open(self._db_loc, "r", encoding="utf8") as f:
            return json.loads(f.read())

    def _write_database(self, db: Dict) -> None:
        with open(self._db_loc, "w", encoding="utf8") as f:
            json.dump(db, f, indent=4)
        self._db = self.__connect_database()


class JsonUserRepository(UserRepository, JsonRepository):
    def __init__(self, db_loc: Optional[str] = None) -> None:
        db_loc = db_loc or "src/db/user.json"
        super().__init__(db_loc=db_loc)

    def save(self, user: UserModel) -> None:
        super().save(user=user)  # Confirm parent's signiture

        self._db[user.username] = user.dict(exclude={"password"})
        self._write_database(db=self._db)

    def exists_by_username(self, username: str) -> bool:
        super().exists_by_username(username=username)

        existed_user = self._db.get(username)
        rst = True if existed_user is not None else False

        return rst
