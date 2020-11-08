"""empty message

Revision ID: f6e9f0391227
Revises: 
Create Date: 2020-10-22 00:53:57.237525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6e9f0391227'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nid', sa.Integer(), nullable=True),
    sa.Column('kid', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('nickname', sa.String(length=100), nullable=True),
    sa.Column('push_token', sa.String(length=100), nullable=True),
    sa.Column('get_push', sa.Boolean(), nullable=True),
    sa.Column('device', sa.String(length=1), nullable=True),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.Column('regdate', sa.DateTime(), nullable=True),
    sa.Column('last_logged_in', sa.DateTime(), nullable=True),
    sa.Column('current_logged_in', sa.DateTime(), nullable=True),
    sa.Column('access_token', sa.String(length=100), nullable=True),
    sa.Column('refresh_token', sa.String(length=100), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('kid'),
    sa.UniqueConstraint('nid'),
    sa.UniqueConstraint('push_token'),
    mysql_collate='utf8_unicode_ci'
    )
    op.create_table('document',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('content', sa.String(length=4000), nullable=False),
    sa.Column('doc_type', sa.String(length=20), nullable=False),
    sa.Column('regdate', sa.DateTime(), nullable=True),
    sa.Column('last_update_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=1), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8_unicode_ci'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document')
    op.drop_table('user')
    # ### end Alembic commands ###
