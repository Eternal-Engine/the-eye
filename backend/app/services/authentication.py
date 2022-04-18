from app.db.errors import EntityDoesNotExist
from app.db.repositories import users as users_repo


async def check_username_is_taken(repo: users_repo.UsersRepository, username: str) -> bool:
    try:
        await repo.get_user_by_username(username=username)
    except EntityDoesNotExist:
        return False

    return True


async def check_email_is_taken(repo: users_repo.UsersRepository, email: str) -> bool:
    try:
        await repo.get_user_by_email(email=email)
    except EntityDoesNotExist:
        return False

    return True


async def authenticate_user(repo: users_repo.UsersRepository, username: str, password: str):

    try:
        await repo.get_user_by_username(username=username)
    except EntityDoesNotExist:
        return False
    else:
        user_in_db = await repo.get_user_by_username(username=username)
        if not user_in_db.check_password(password=password):
            return False
        return user_in_db
