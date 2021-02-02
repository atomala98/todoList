"""user authentication

Revision ID: 2282e6dbf7b5
Revises: 9b29cf2e0c13
Create Date: 2021-02-02 18:06:12.767026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2282e6dbf7b5'
down_revision = '9b29cf2e0c13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('authenticated', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_user_authenticated'), 'user', ['authenticated'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_authenticated'), table_name='user')
    op.drop_column('user', 'authenticated')
    # ### end Alembic commands ###
