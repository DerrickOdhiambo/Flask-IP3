"""add a column for the comments relationship between itself and the posts

Revision ID: 29cfe32833f4
Revises: 4471b8e4d6e7
Create Date: 2020-09-24 11:03:36.439953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29cfe32833f4'
down_revision = '4471b8e4d6e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('pitch_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comments', 'posts', ['pitch_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'pitch_id')
    # ### end Alembic commands ###
