import sqlalchemy

from app.db.database import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=False, index=True),
    sqlalchemy.Column("email", sqlalchemy.String, nullable=False, index=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column(
        "updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), server_onupdate=sqlalchemy.func.now()
    ),
    sqlalchemy.Column(
        "last_logged_in_at",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
        server_onupdate=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column(
        "username_updated_at",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
        server_onupdate=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column(
        "email_updated_at",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
        server_onupdate=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column(
        "password_updated_at",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
        server_onupdate=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column("is_publisher", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("is_premium_account", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("is_verified", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean, default=True),
)
