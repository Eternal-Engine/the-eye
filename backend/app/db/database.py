import databases
import sqlalchemy

from app.core.config import get_settings
from app.core.settings.app_base_settings import EnvTypes

settings = get_settings(app_env=EnvTypes.DEV)
DATABASE_URL = settings.database_url

# Databases query builder
database = databases.Database(DATABASE_URL)

# SQLAlchemy native for database transaction
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata = sqlalchemy.MetaData()
