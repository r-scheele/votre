"""generate the rest of the columns and tables

Revision ID: 3846c54a064e
Revises: e813d7543ab2
Create Date: 2021-12-22 10:31:59.991389

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3846c54a064e'
down_revision = 'e813d7543ab2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=140), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('path', sa.Text(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_created_at'), 'comments', ['created_at'], unique=False)
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_index(op.f('ix_comments_path'), 'comments', ['path'], unique=False)
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_likes_id'), 'likes', ['id'], unique=False)
    op.alter_column('posts', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_index(op.f('ix_posts_content'), 'posts', ['content'], unique=False)
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=False)
    op.drop_constraint('post_users_fk', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['owner_id'], ['id'])
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False))
    op.add_column('users', sa.Column('role', sa.String(length=128), server_default='user', nullable=False))
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.drop_column('users', 'role')
    op.drop_column('users', 'is_active')
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('post_users_fk', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_posts_title'), table_name='posts')
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_index(op.f('ix_posts_content'), table_name='posts')
    op.alter_column('posts', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_index(op.f('ix_likes_id'), table_name='likes')
    op.drop_table('likes')
    op.drop_index(op.f('ix_comments_path'), table_name='comments')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_index(op.f('ix_comments_created_at'), table_name='comments')
    op.drop_table('comments')
    # ### end Alembic commands ###
