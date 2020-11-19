"""empty message

Revision ID: 9a9b8daa709a
Revises: a5b0cf2f0f2e
Create Date: 2020-11-19 18:12:33.532577

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9a9b8daa709a'
down_revision = 'a5b0cf2f0f2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'device',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=1),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'device',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=1),
               nullable=True)
    # ### end Alembic commands ###