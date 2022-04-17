# type: ignore
from app.db.repositories import base as base_repo


class UsersRepository(base_repo.BaseRepository):
    async def create_user():
        pass

    async def read_users():
        pass
