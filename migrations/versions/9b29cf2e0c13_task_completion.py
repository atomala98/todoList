"""task completion

Revision ID: 9b29cf2e0c13
Revises: de1c12e1339a
Create Date: 2021-01-25 18:17:20.304201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b29cf2e0c13'
down_revision = 'de1c12e1339a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('is_completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'is_completed')
    # ### end Alembic commands ###
