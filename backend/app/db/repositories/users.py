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
    ) -> users_domain.UserInDB:

        db_user = users_domain.UserInDB(username=username, email=email)
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

    async def read_users(self):
        pass
