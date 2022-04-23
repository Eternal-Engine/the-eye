# type: ignore
from typing import List, Optional, Union

from asyncpg import connection as asyncpg_conn

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.publishers import Publisher, PublisherInDB
from app.models.domain.users import User

PublisherProfile = Union[User, Publisher]


class PublishersRepository(BaseRepository):
    def __init__(self, conn: asyncpg_conn.Connection):
        super().__init__(conn)
        self._users_repo = UsersRepository(conn)

    async def create_publisher_by_username(
        self,
        *,
        username: str,
        name: str = "",
        profile_picture: str = "",
        banner: str = "",
        bio: str = "",
        address: str = "",
        postal_code: str = "",
        state: str = "",
        country: str = "",
        office_phone_number: str = "",
        mobile_phone_number: str = "",
    ) -> PublisherProfile:

        db_user = await self._users_repo.get_user_by_username(username=username)

        try:
            db_publisher = await self.get_publisher_by_user_id(id=db_user.id_)

        except EntityDoesNotExist:

            db_publisher = PublisherInDB(
                name=name,
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

                await queries.create_new_publisher(
                    self.connection,
                    name=db_publisher.name,
                    profile_picture=db_publisher.profile_picture,
                    banner=db_publisher.banner,
                    bio=db_publisher.bio,
                    address=db_publisher.address,
                    postal_code=db_publisher.postal_code,
                    state=db_publisher.state,
                    country=db_publisher.country,
                    office_phone_number=db_publisher.office_phone_number,
                    mobile_phone_number=db_publisher.mobile_phone_number,
                    user_id=db_publisher.user_id,
                )

        return db_publisher

    async def get_publishers(self) -> List[PublisherInDB]:
        async with self.connection.transaction():
            db_publishers = await queries.read_publishers(self.connection)
            db_publishers_list = []

            for db_publisher in db_publishers:

                db_publishers_list.append(PublisherInDB(**db_publisher))

            return db_publishers_list

    async def get_publisher_by_user_id(self, *, id: int) -> PublisherInDB:

        db_publisher = await queries.read_publisher_by_user_id(self.connection, user_id=id)

        if db_publisher:

            return PublisherInDB(**db_publisher)

        raise EntityDoesNotExist(f"Publisher with id {id} doesn't exist!")

    async def update_publisher_by_user_id(
        self,
        *,
        user_id: int,
        name: Optional[str] = None,
        profile_picture: Optional[str] = None,
        banner: Optional[str] = None,
        bio: Optional[str] = None,
        address: Optional[str] = None,
        postal_code: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        office_phone_number: Optional[str] = None,
        mobile_phone_number: Optional[str] = None,
    ) -> PublisherInDB:

        db_publisher = await self.get_publisher_by_user_id(id=user_id)

        if db_publisher:
            db_publisher.name = name or db_publisher.name
            db_publisher.profile_picture = profile_picture or db_publisher.profile_picture
            db_publisher.banner = banner or db_publisher.banner
            db_publisher.bio = bio or db_publisher.bio
            db_publisher.address = address or db_publisher.address
            db_publisher.postal_code = postal_code or db_publisher.postal_code
            db_publisher.state = state or db_publisher.state
            db_publisher.country = country or db_publisher.country
            db_publisher.office_phone_number = office_phone_number or db_publisher.office_phone_number
            db_publisher.mobile_phone_number = mobile_phone_number or db_publisher.mobile_phone_number

            async with self.connection.transaction():
                db_publisher.updated_at = await queries.update_publisher_by_id(
                    self.connection,
                    id=user_id,
                    new_name=db_publisher.name,
                    new_profile_picture=db_publisher.profile_picture,
                    new_banner=db_publisher.banner,
                    new_bio=db_publisher.bio,
                    new_address=db_publisher.address,
                    new_postal_code=db_publisher.postal_code,
                    new_state=db_publisher.state,
                    new_country=db_publisher.country,
                    new_office_phone_number=db_publisher.office_phone_number,
                    new_mobile_phone_number=db_publisher.mobile_phone_number,
                )

            return db_publisher

        raise EntityDoesNotExist("Publisher with that ID does not exist!")
