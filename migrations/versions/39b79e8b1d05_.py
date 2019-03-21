"""empty message

Revision ID: 39b79e8b1d05
Revises: f446b9619bae
Create Date: 2019-03-21 09:37:15.998384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39b79e8b1d05'
down_revision = 'f446b9619bae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'active')
    # ### end Alembic commands ###
