"""Add Post table

Revision ID: edc64ce5651c
Revises: 
Create Date: 2021-11-19 12:23:29.180149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edc64ce5651c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('is_published', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entry')
    # ### end Alembic commands ###
