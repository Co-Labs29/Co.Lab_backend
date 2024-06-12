"""empty message

Revision ID: 538ddfbebc32
Revises: 18e44419ef6b
Create Date: 2024-06-12 11:43:09.866655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '538ddfbebc32'
down_revision = '18e44419ef6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(), nullable=True))

    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('complete', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.drop_column('complete')

    with op.batch_alter_table('chores', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
