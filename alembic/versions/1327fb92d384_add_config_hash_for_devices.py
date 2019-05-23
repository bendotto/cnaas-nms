"""add config hash for devices

Revision ID: 1327fb92d384
Revises: d1e7569c57a2
Create Date: 2019-05-23 08:40:31.711177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1327fb92d384'
down_revision = 'd1e7569c57a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('config_hash', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'config_hash')
    # ### end Alembic commands ###
