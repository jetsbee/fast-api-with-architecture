import inspect
import json

from typing import Dict, Optional

from ..domain.repositories.user import UserRepository
from ..domain.models.user import UserModel
from ....utils import run_async


class JsonRepository:
    def __init__(self, db_loc: str) -> None:
        if inspect.stack()[1][3] not in ["async_init", "__init__"]:
            raise Exception(f"Use async_init() in {self.__class__.__name__}.")

        self._db_loc = db_loc

    @classmethod
    async def async_init(cls, db_loc: str):
        self = cls(db_loc=db_loc)
        self._db = await self.__connect_database()

        return self

    @run_async
    def __connect_database(self) -> Dict:
        with open(self._db_loc, "r", encoding="utf8") as f:
            return json.loads(f.read())

    @run_async
    def __renew_database(self, db: Dict) -> None:
        with open(self._db_loc, "w", encoding="utf8") as f:
            json.dump(db, f, indent=4)

    async def _write_database(self, db: Dict) -> None:
        await self.__renew_database(db=db)
        self._db = await self.__connect_database()


class JsonUserRepository(UserRepository, JsonRepository):
    def __init__(self, db_loc: Optional[str] = None) -> None:
        if inspect.stack()[1][3] != "async_init":
            raise Exception(f"Use async_init() in {self.__class__.__name__}.")

        super().__init__(db_loc=db_loc)

    @classmethod
    async def async_init(cls, db_loc: str = "src/db/user.json"):
        self = await super().async_init(db_loc=db_loc)

        return self

    async def save(self, user: UserModel) -> None:
        await super().save(user=user)  # Confirm parent's signiture

        self._db[user.username] = user.dict(exclude={"password"})
        await self._write_database(db=self._db)

    def exists_by_username(self, username: str) -> bool:
        super().exists_by_username(username=username)

        existed_user = self._db.get(username)
        rst = True if existed_user is not None else False

        return rst
