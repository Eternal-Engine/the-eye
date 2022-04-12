from app.db.database import database
from app.models.db_models import users as db_users
from app.models.schemas import users as user_schemas


async def create_user(payload: user_schemas.UserInCreate):

    query = db_users.insert().values(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        is_publisher=payload.is_publisher,
        is_premium_account=payload.is_premium_account,
        is_verified=payload.is_verified,
        is_active=payload.is_active,
    )

    return await database.execute(query=query)
