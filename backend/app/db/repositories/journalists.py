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

    async def create_journalist_profile_from_getting_user_by_username(
        self,
        *,
        username: str,
        first_name: str = "",
        last_name: str = "",
        profile_picture: str = "",
        banner: str = "",
        bio: str = "",
        address: str = "",
        postal_code: str = "",
        state: str = "",
        country: str = "",
        office_phone_number: str = "",
        mobile_phone_number: str = "",
        journalist_profile: Optional[JournalistProfile],
    ) -> JournalistProfile:

        db_user = await self._users_repo.get_user_by_username(username=username)

        try:
            journalist_profile = await self.get_journalist_by_id(id=db_user.id_)

        except EntityDoesNotExist:

            journalist_profile = JournalistInDB(
                first_name=first_name,
                last_name=last_name,
                profile_picture=profile_picture,
                banner=banner,
                bio=bio,
                address=address,
                postal_code=postal_code,
                state=state,
                country=country,
                office_phone_number=office_phone_number,
                mobile_phone_number=mobile_phone_number,
                user_id=db_user.id_,
            )

            async with self.connection.transaction():

                await queries.create_new_journalist(
                    self.connection,
                    first_name=journalist_profile.first_name,
                    last_name=journalist_profile.last_name,
                    profile_picture=journalist_profile.profile_picture,
                    banner=journalist_profile.banner,
                    bio=journalist_profile.bio,
                    address=journalist_profile.address,
                    postal_code=journalist_profile.postal_code,
                    state=journalist_profile.state,
                    country=journalist_profile.country,
                    office_phone_number=journalist_profile.office_phone_number,
                    mobile_phone_number=journalist_profile.mobile_phone_number,
                    user_id=journalist_profile.user_id,
                )

        return journalist_profile

    async def get_journalist_by_id(self, *, id: int) -> JournalistInDB:

        db_journalist = await queries.read_journalist_by_user_id(self.connection, user_id=id)

        if db_journalist:

            return JournalistInDB(**db_journalist)

        raise EntityDoesNotExist(f"User with id {id} does not exist!")

    async def update_journalist_profile(
        self,
        *,
        journalist: Journalist,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        profile_picture: Optional[str] = None,
        banner: Optional[str] = None,
        bio: Optional[str] = None,
        address: Optional[str] = None,
        postal_code: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        office_phone_number: Optional[str] = None,
        mobile_phone_number: Optional[str] = None,
    ) -> JournalistInDB:

        db_journalist = await self.get_journalist_by_id(id=journalist.user_id)

        if db_journalist:
            db_journalist.first_name = first_name or db_journalist.first_name
            db_journalist.last_name = last_name or db_journalist.last_name
            db_journalist.profile_picture = profile_picture or db_journalist.profile_picture
            db_journalist.banner = banner or db_journalist.banner
            db_journalist.bio = bio or db_journalist.bio
            db_journalist.address = address or db_journalist.address
            db_journalist.postal_code = postal_code or db_journalist.postal_code
            db_journalist.state = state or db_journalist.state
            db_journalist.country = country or db_journalist.country
            db_journalist.office_phone_number = office_phone_number or db_journalist.office_phone_number
            db_journalist.mobile_phone_number = mobile_phone_number or db_journalist.mobile_phone_number

            async with self.connection.transaction():
                db_journalist.updated_at = await queries.update_journalist_by_id(
                    self.connection,
                    id=journalist.user_id,
                    new_first_name=db_journalist.first_name,
                    new_last_name=db_journalist.last_name,
                    new_profile_picture=db_journalist.profile_picture,
                    new_banner=db_journalist.banner,
                    new_bio=db_journalist.bio,
                    new_address=db_journalist.address,
                    new_postal_code=db_journalist.postal_code,
                    new_state=db_journalist.state,
                    new_country=db_journalist.country,
                    new_office_phone_number=db_journalist.office_phone_number,
                    new_mobile_phone_number=db_journalist.mobile_phone_number,
                )

            return db_journalist

        raise EntityDoesNotExist("User with that ID does not exist!")
