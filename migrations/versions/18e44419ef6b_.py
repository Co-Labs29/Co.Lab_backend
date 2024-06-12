"""empty message

Revision ID: 18e44419ef6b
Revises: 46fb47f64f88
Create Date: 2024-06-12 11:22:22.512130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18e44419ef6b'
down_revision = '46fb47f64f88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.drop_column('_complete')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('goal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_complete', sa.BOOLEAN(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
