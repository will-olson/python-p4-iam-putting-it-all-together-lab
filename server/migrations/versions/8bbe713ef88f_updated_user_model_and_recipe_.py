"""Updated user model and recipe relationship

Revision ID: 8bbe713ef88f
Revises: ae4db40a9e7a
Create Date: 2024-12-15 11:59:04.072848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bbe713ef88f'
down_revision = 'ae4db40a9e7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.alter_column('instructions',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('bio',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('bio',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.alter_column('instructions',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=False)

    # ### end Alembic commands ###
