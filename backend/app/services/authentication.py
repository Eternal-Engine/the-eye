from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository


async def check_username_is_taken(users_repo: UsersRepository, username: str) -> bool:
    try:
        await users_repo.get_user_by_username(username=username)

    except EntityDoesNotExist:
        return False

    return True


async def check_email_is_taken(users_repo: UsersRepository, email: str) -> bool:
    try:
        await users_repo.get_user_by_email(email=email)

    except EntityDoesNotExist:
        return False

    return True


async def authenticate_user(users_repo: UsersRepository, email: str, password: str):

    try:
        user_in_db = await users_repo.get_user_by_email(email=email)

    except EntityDoesNotExist:
        return False

    else:
        if not user_in_db.check_password(password=password):
            return False

    return user_in_db
