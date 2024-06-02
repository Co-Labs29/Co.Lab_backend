"""empty message

Revision ID: 48d33e8ce456
Revises: f5fd21d6e5a9
Create Date: 2024-06-02 18:46:01.922178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48d33e8ce456'
down_revision = 'f5fd21d6e5a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('child', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('child', schema=None) as batch_op:
        batch_op.drop_column('img')

    # ### end Alembic commands ###
