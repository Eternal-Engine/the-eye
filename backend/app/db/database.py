from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import get_settings, log
from app.core.settings.app_base_settings import EnvTypes

settings = get_settings(app_env=EnvTypes.DEV)
DATABASE_URL = settings.database_url
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
Base = declarative_base()


async def init_db():

    log.info("Set up database...")
    # Initialize db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session():

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        yield session
