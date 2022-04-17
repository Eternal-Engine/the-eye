from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories import base as base_repo
from app.models.domain import users as users_domain


class UsersRepository(base_repo.BaseRepository):
    async def create_user(
        self,
        *,
        username: str,
        email: str,
        password: str,
    ) -> users_domain.UserInDB:  # type: ignore

        db_user = users_domain.UserInDB(username=username, email=email)  # type: ignore
        db_user.change_password(new_password=password)

        async with self.connection.transaction():

            user_row = await queries.create_new_user(
                self.connection,
                username=db_user.username,
                email=db_user.email,
                salt=db_user.salt,
                hashed_password=db_user.hashed_password,
            )

        return db_user.copy(update=dict(user_row))

    async def read_users(self) -> users_domain.UserInDB:  # type: ignore
        async with self.connection.transaction():
            user_rows = await queries.read_users(self.connection)
            list_of_all_user_rows = []

            for user_row in user_rows:

                list_of_all_user_rows.append(users_domain.UserInDB(**user_row))  # type: ignore

            return list_of_all_user_rows

    async def get_user_by_id(self, *, user_id: int) -> users_domain.UserInDB:

        user_row = await queries.read_user_by_id(self.connection, id=user_id)

        if user_row:

            return users_domain.UserInDB(**user_row)

        raise EntityDoesNotExist("User with id {user_id} does not exist!")

    async def get_user_by_username(self, *, username: str) -> users_domain.UserInDB:

        user_row = await queries.read_user_by_username(self.connection, username=username)

        if user_row:

            return users_domain.UserInDB(**user_row)

        raise EntityDoesNotExist("User with username {username} does not exist!")

    async def get_user_by_email(self, *, user_email: str) -> users_domain.UserInDB:

        user_row = await queries.read_user_by_email(self.connection, email=user_email)

        if user_row:

            return users_domain.UserInDB(**user_row)

        raise EntityDoesNotExist("User with email {user_email} does not exist!")
