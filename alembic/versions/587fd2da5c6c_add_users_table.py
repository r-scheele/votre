"""add users table

Revision ID: 587fd2da5c6c
Revises: 4ecf22098855
Create Date: 2021-12-22 09:32:21.147402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '587fd2da5c6c'
down_revision = '4ecf22098855'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass
