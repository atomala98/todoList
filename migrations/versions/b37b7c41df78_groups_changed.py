"""Groups changed

Revision ID: b37b7c41df78
Revises: d30fa46ac928
Create Date: 2021-02-12 13:13:23.353176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b37b7c41df78'
down_revision = 'd30fa46ac928'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('name', sa.String(length=64), nullable=True))
    op.alter_column('message', 'receiver_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.create_foreign_key(None, 'message', 'user', ['receiver_id'], ['id'])
    op.create_foreign_key(None, 'message', 'user', ['sender_id'], ['id'])
    op.drop_column('message', 'user_id')
    op.drop_column('message', 'author')
    op.drop_column('message', 'author_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('author_id', sa.INTEGER(), nullable=True))
    op.add_column('message', sa.Column('author', sa.VARCHAR(length=40), nullable=True))
    op.add_column('message', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.create_foreign_key(None, 'message', 'user', ['user_id'], ['id'])
    op.alter_column('message', 'receiver_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('group', 'name')
    # ### end Alembic commands ###
