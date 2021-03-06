"""my message

Revision ID: abb37a25ac23
Revises: 4e86b28ce548
Create Date: 2022-02-02 15:28:42.991066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abb37a25ac23'
down_revision = '4e86b28ce548'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'profile_pic',
                existing_type=sa.String(),
                type_=sa.Boolean(),
                existing_nullable=True,
               postgresql_using='profile_pic::boolean')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
