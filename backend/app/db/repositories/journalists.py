# type: ignore
from typing import Optional, Union

from asyncpg import connection as asyncpg_conn

from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.journalists import Journalist, JournalistInDB
from app.models.domain.users import User

JournalistProfile = Union[User, Journalist]


class JournalistsRepository(BaseRepository):
    def __init__(self, conn: asyncpg_conn.Connection):
        super().__init__(conn)
        self._users_repo = UsersRepository(conn)

    async def get_journalist_profile_by_username(
        self,
        *,
        username: str,
        first_name: str = "",
        last_name: str = "",
        profile_picture: str = "",
        bio: str = "",
        journalist_profile: Optional[JournalistProfile]
    ) -> JournalistProfile:

        db_user = await self._users_repo.get_user_by_username(username=username)

        db_journalist = JournalistInDB(
            username=db_user.username,
            email=db_user.email,
            first_name=first_name,
            last_name=last_name,
            profile_picture=profile_picture,
            bio=bio,
            user_id=db_user.id_,
        )

        async with self.connection.transaction():

            await queries.create_new_journalist(
                self.connection,
                first_name=db_journalist.first_name,
                last_name=db_journalist.last_name,
                profile_picture=db_journalist.profile_picture,
                bio=db_journalist.bio,
                user_id=db_journalist.user_id,
            )

        journalist_profile = Journalist(
            username=db_journalist.username,
            email=db_journalist.email,
            first_name=db_journalist.first_name,
            last_name=db_journalist.last_name,
            profile_picture=db_journalist.profile_picture,
            bio=db_journalist.bio,
            user_id=db_journalist.user_id,
        )

        return journalist_profile
