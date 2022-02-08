"""Added description

Revision ID: 440717fdd550
Revises: 
Create Date: 2022-01-31 14:00:34.489660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '440717fdd550'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('testtable')
    op.add_column('users', sa.Column('self_description', sa.String(), nullable=True))
    op.add_column('users', sa.Column('project_description', sa.String(), nullable=True))
    op.drop_column('users', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'project_description')
    op.drop_column('users', 'self_description')
    op.create_table('testtable',

    )
    # ### end Alembic commands ###
