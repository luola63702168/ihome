"""add trade_no

Revision ID: 857c87d9ba50
Revises: d47793a01d98
Create Date: 2019-11-24 20:54:09.810138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '857c87d9ba50'
down_revision = 'd47793a01d98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ih_order_info', sa.Column('trade_no', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ih_order_info', 'trade_no')
    # ### end Alembic commands ###
