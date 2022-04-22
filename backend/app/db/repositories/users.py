# type: ignore
from typing import Any, List, Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.users import User, UserInDB


class UsersRepository(BaseRepository):
    async def create_user(
        self,
        *,
        username: str,
        email: str,
        password: str,
        is_publisher: bool = False,
        is_verified: bool = False,
        is_active: bool = True,
    ) -> UserInDB:

        db_user = UserInDB(
            username=username, email=email, is_publisher=is_publisher, is_verified=is_verified, is_active=is_active
        )
        db_user.change_password(new_password=password)

        async with self.connection.transaction():

            new_user = await queries.create_new_user(
                self.connection,
                username=db_user.username,
                email=db_user.email,
                salt=db_user.salt,
                hashed_password=db_user.hashed_password,
                is_publisher=db_user.is_publisher,
                is_verified=db_user.is_verified,
                is_active=db_user.is_active,
            )

        return db_user.copy(update=dict(new_user))

    async def get_users(self) -> List[UserInDB]:
        async with self.connection.transaction():
            db_users = await queries.read_users(self.connection)
            db_users_list = []

            for db_user in db_users:

                db_users_list.append(UserInDB(**db_user))

            return db_users_list

    async def get_user_by_id(self, *, id: int) -> UserInDB:

        db_user = await queries.read_user_by_id(self.connection, id=id)

        if db_user:

            return UserInDB(**db_user)

        raise EntityDoesNotExist(f"User with id {id} does not exist!")

    async def get_user_by_username(self, *, username: str) -> UserInDB:

        db_user = await queries.read_user_by_username(self.connection, username=username)

        if db_user:

            return UserInDB(**db_user)

        raise EntityDoesNotExist(f"User with username {username} does not exist!")

    async def get_user_by_email(self, *, email: str) -> UserInDB:

        db_user = await queries.read_user_by_email(self.connection, email=email)

        if db_user:

            return UserInDB(**db_user)

        raise EntityDoesNotExist(f"User with email {email} does not exist!")

    async def update_user(
        self,
        *,
        user: User,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        is_publisher: Optional[bool] = None,
    ) -> UserInDB:

        db_user = await self.get_user_by_id(id=user.id_)

        if db_user:
            db_user.username = username or db_user.username
            db_user.email = email or db_user.email
            db_user.is_publisher = is_publisher or db_user.is_publisher

            if password:
                db_user.change_password(password)

            async with self.connection.transaction():
                db_user.updated_at = await queries.update_user_by_id(
                    self.connection,
                    id=user.id_,
                    username=user.username,
                    new_username=db_user.username,
                    new_email=db_user.email,
                    new_salt=db_user.salt,
                    new_password=db_user.hashed_password,
                    new_is_publisher=db_user.is_publisher,
                )

            return db_user

        raise EntityDoesNotExist("User with that ID does not exist!")

    async def delete_user(self, *, id: int) -> Any:

        try:
            return await queries.delete_user_by_id(self.connection, id=id)

        except EntityDoesNotExist as value_error:

            raise ValueError(f"User with id {id} does not exist!") from value_error
