"""empty message

Revision ID: ebcae4b14bfe
Revises: 72b55287eb0d
Create Date: 2021-02-13 16:26:35.706932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebcae4b14bfe'
down_revision = '72b55287eb0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('admin_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group', 'admin_id')
    # ### end Alembic commands ###