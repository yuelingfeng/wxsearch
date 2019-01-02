"""empty message

Revision ID: adba088e1b8f
Revises: c1ea117506ec
Create Date: 2018-10-25 14:11:27.326596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adba088e1b8f'
down_revision = 'c1ea117506ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('sn', sa.String(length=8), nullable=False),
    sa.Column('ipaddress', sa.String(length=15), nullable=False),
    sa.Column('state', sa.String(length=1), nullable=True),
    sa.Column('duedate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('company')
    # ### end Alembic commands ###