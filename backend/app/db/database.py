from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

# Get the database url based on the environment settings
settings = get_settings()

# Connect database with SQLAlchemy
DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# As the base class for db objects in models.py
Base = declarative_base()


# Initialize db session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
