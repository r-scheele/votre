"""add content column to post table

Revision ID: 4ecf22098855
Revises: cd99e72bc839
Create Date: 2021-12-22 09:21:57.579434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ecf22098855'
down_revision = 'cd99e72bc839'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
