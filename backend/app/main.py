from fastapi import FastAPI, status

from app.core.config import get_settings, log
from app.core.settings.app_base_settings import EnvTypes
from app.db.database import database, engine, metadata
from app.models.db_models import users as db_users
from app.models.schemas import users as user_schemas

# metadata.drop_all(engine)
metadata.create_all(engine)

settings = get_settings(app_env=EnvTypes.DEV)
app = FastAPI(**settings.fastapi_kwargs)


@app.on_event("startup")
async def startup():
    await database.connect()
    log.info("Database is successfully CONNECTED...")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    log.info("Database is DISCONNECTED...")


@app.get("/app_settings/", tags=["App Settings"])
async def get_app_settings():

    return {
        "environment": settings.app_env,
    }


@app.post("/users/create/", response_model=user_schemas.UserInResponse, status_code=status.HTTP_201_CREATED)
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

    new_user = await database.execute(query)

    response_object = {
        "id": new_user,
        "username": payload.username,
        "email": payload.email,
        "is_publisher": payload.is_publisher,
        "is_premium_account": payload.is_premium_account,
        "is_verified": payload.is_verified,
        "is_active": payload.is_active,
    }

    return response_object
