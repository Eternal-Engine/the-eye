# type: ignore
from typing import Any, List, Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.users import User, UserInDB


class UsersRepository(BaseRepository):
    async def create_new_user(
        self,
        *,
        username: str,
        email: str,
        password: str,
    ) -> UserInDB:

        db_user = UserInDB(username=username, email=email)
        db_user.change_password(new_password=password)

        async with self.connection.transaction():

            user_row = await queries.create_user(
                self.connection,
                username=db_user.username,
                email=db_user.email,
                salt=db_user.salt,
                hashed_password=db_user.hashed_password,
            )

        return db_user.copy(update=dict(user_row))

    async def get_users(self) -> List[UserInDB]:
        async with self.connection.transaction():
            user_rows = await queries.read_users(self.connection)
            list_of_all_user_rows = []

            for user_row in user_rows:

                list_of_all_user_rows.append(UserInDB(**user_row))

            return list_of_all_user_rows

    async def get_user_by_id(self, *, id: int) -> UserInDB:

        user_row = await queries.read_user_by_id(self.connection, id=id)

        if user_row:

            return UserInDB(**user_row)

        raise EntityDoesNotExist(f"User with id {id} does not exist!")

    async def get_user_by_username(self, *, username: str) -> UserInDB:

        user_row = await queries.read_user_by_username(self.connection, username=username)

        if user_row:

            return UserInDB(**user_row)

        raise EntityDoesNotExist(f"User with username {username} does not exist!")

    async def get_user_by_email(self, *, email: str) -> UserInDB:

        user_row = await queries.read_user_by_email(self.connection, email=email)

        if user_row:

            return UserInDB(**user_row)

        raise EntityDoesNotExist(f"User with email {email} does not exist!")

    async def revise_user_by_id(
        self,
        *,
        user: User,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> UserInDB:

        user_in_db = await self.get_user_by_id(id=user.id)

        if user_in_db:
            user_in_db.username = username or user_in_db.username
            user_in_db.email = email or user_in_db.email

            if password:
                user_in_db.change_password(password)

            async with self.connection.transaction():
                user_in_db.updated_at = await queries.update_user_by_id(
                    self.connection,
                    id=user.id,
                    username=user.username,
                    new_username=user_in_db.username,
                    new_email=user_in_db.email,
                    new_salt=user_in_db.salt,
                    new_password=user_in_db.hashed_password,
                )

            return user_in_db

        raise EntityDoesNotExist("User with that ID does not exist!")

    async def revise_user_by_username(
        self,
        *,
        user: User,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> UserInDB:

        user_in_db = await self.get_user_by_username(username=user.username)

        if user_in_db:
            user_in_db.username = username or user_in_db.username
            user_in_db.email = email or user_in_db.email

            if password:
                user_in_db.change_password(password)

            async with self.connection.transaction():
                user_in_db.updated_at = await queries.update_user_by_username(
                    self.connection,
                    username=user.username,
                    new_username=user_in_db.username,
                    new_email=user_in_db.email,
                    new_salt=user_in_db.salt,
                    new_password=user_in_db.hashed_password,
                )

            return user_in_db

        raise EntityDoesNotExist("User with that username does not exist!")

    async def remove_user_by_id(
        self,
        *,
        id: int,
    ) -> Any:

        user_in_db = await self.get_user_by_id(id=id)

        if user_in_db:
            async with self.connection.transaction():
                user_in_db = await queries.delete_user_by_id(self.connection, id=id)
            if not user_in_db:

                return "User is successfully deleted from database!"

            return user_in_db

        raise EntityDoesNotExist(f"User with username {id} does not exist!")

    async def remove_user_by_username(
        self,
        *,
        username: str,
    ) -> Any:

        user_in_db = await self.get_user_by_username(username=username)

        if user_in_db:

            async with self.connection.transaction():
                user_in_db = await queries.delete_user_by_username(self.connection, username=username)

            if not user_in_db:

                return "User is successfully deleted from database!"

            return user_in_db

        raise EntityDoesNotExist(f"User with username {username} does not exist!")
