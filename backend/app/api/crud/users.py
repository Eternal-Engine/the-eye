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


async def get_all_users():

    query = db_users.select()

    return await database.fetch_all(query=query)


async def get_user_by_id(id: int):

    query = db_users.select().where(id == db_users.c.id)

    return await database.fetch_one(query=query)


async def update_user(id: int, payload: user_schemas.UserInUpdate):

    query = (
        db_users.update()
        .where(id == db_users.c.id)
        .values(
            username=payload.username,
            email=payload.email,
            is_publisher=payload.is_publisher,
            is_premium_account=payload.is_premium_account,
            is_verified=payload.is_verified,
            is_active=payload.is_active,
        )
        .returning(db_users.c.id)
    )

    return await database.execute(query=query)


async def delete_user(id: int):

    query = db_users.delete().where(id == db_users.c.id)

    return await database.execute(query=query)
