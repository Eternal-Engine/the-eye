"""create users table

Revision ID: 19b20050fc3e
Revises:
Create Date: 2022-04-18 00:56:36.134341

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "19b20050fc3e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(50)),
        sa.Column("email", sa.String(50)),
        sa.Column("salt", sa.String),
        sa.Column("hashed_password", sa.String),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )


def downgrade():
    op.drop_table("users")
