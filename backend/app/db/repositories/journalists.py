# type: ignore
from typing import Optional, Union

from asyncpg import connection as asyncpg_conn

from app.db.errors import EntityDoesNotExist
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
        journalist_profile: Optional[JournalistProfile],
    ) -> JournalistProfile:

        db_user = await self._users_repo.get_user_by_username(username=username)

        db_journalist = JournalistInDB(
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
            first_name=db_journalist.first_name,
            last_name=db_journalist.last_name,
            profile_picture=db_journalist.profile_picture,
            bio=db_journalist.bio,
            user_id=db_journalist.user_id,
        )

        return journalist_profile

    async def get_journalist_by_id(self, *, id: int) -> JournalistInDB:

        db_journalist = await queries.read_journalist_by_id(self.connection, id=id)
        print(db_journalist)
        if db_journalist:

            return JournalistInDB(**db_journalist)

        raise EntityDoesNotExist(f"User with id {id} does not exist!")

    async def update_journalist(
        self,
        *,
        journalist: Journalist,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        profile_picture: Optional[str] = None,
        bio: Optional[str] = None,
    ) -> JournalistInDB:

        db_journalist = await self.get_journalist_by_id(id=journalist.user_id)

        if db_journalist:
            db_journalist.first_name = first_name or db_journalist.first_name
            db_journalist.last_name = last_name or db_journalist.last_name
            db_journalist.profile_picture = profile_picture or db_journalist.profile_picture
            db_journalist.bio = bio or db_journalist.bio

            async with self.connection.transaction():
                db_journalist.updated_at = await queries.update_journalist_by_id(
                    self.connection,
                    id=journalist.user_id,
                    new_first_name=db_journalist.first_name,
                    new_last_name=db_journalist.last_name,
                    new_profile_picture=db_journalist.profile_picture,
                    new_bio=db_journalist.bio,
                )

            return db_journalist

        raise EntityDoesNotExist("User with that ID does not exist!")
