"""create tables

Revision ID: a177683deb81
Revises:
Create Date: 2022-04-21 01:55:27.324748

"""
from typing import Tuple

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a177683deb81"
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
    CREATE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS
    $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    )


def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.current_timestamp(),
        ),
    )


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("username", sa.Text, index=True, nullable=False, unique=True),
        sa.Column("email", sa.Text, index=True, nullable=False, unique=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("hashed_password", sa.Text),
        sa.Column("is_publisher", sa.Boolean, default=False),
        sa.Column("is_verified", sa.Boolean, default=False),
        sa.Column("is_active", sa.Boolean, default=True),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_articles_table() -> None:
    op.create_table(
        "articles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("slug", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("headline", sa.VARCHAR, nullable=False),
        sa.Column("description", sa.VARCHAR, nullable=True),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("author_id", sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_article_modtime
            BEFORE UPDATE
            ON articles
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_images_table() -> None:
    op.create_table(
        "images",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("slug", sa.VARCHAR, unique=True, nullable=False, index=True),
        sa.Column("path", sa.Text, nullable=False),
        sa.Column("title", sa.VARCHAR, nullable=True),
        sa.Column("alt", sa.Text, nullable=False),
        sa.Column("article_id", sa.Integer, sa.ForeignKey("articles.id", ondelete="SET NULL")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_image_modtime
            BEFORE UPDATE
            ON images
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_videos_table() -> None:
    op.create_table(
        "videos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("slug", sa.VARCHAR, unique=True, nullable=False, index=True),
        sa.Column("path", sa.Text, nullable=False),
        sa.Column("title", sa.VARCHAR, nullable=True),
        sa.Column("alt", sa.Text, nullable=False),
        sa.Column("article_id", sa.Integer, sa.ForeignKey("articles.id", ondelete="SET NULL")),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_video_modtime
            BEFORE UPDATE
            ON videos
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_users_table()
    create_articles_table()
    create_images_table()
    create_videos_table()


def downgrade() -> None:
    op.drop_table("videos")
    op.drop_table("images")
    op.drop_table("articles")
    op.drop_table("users")
    op.execute("DROP FUNCTION update_updated_at_column")
