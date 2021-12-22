"""add the last columns to posts table

Revision ID: e813d7543ab2
Revises: a1045aed3cc0
Create Date: 2021-12-22 10:05:10.138888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e813d7543ab2'
down_revision = 'a1045aed3cc0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                                     nullable=False, server_default=sa.text("now()")))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
