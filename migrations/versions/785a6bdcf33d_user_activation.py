"""User activation

Revision ID: 785a6bdcf33d
Revises: dff8180648eb
Create Date: 2020-03-30 21:33:58.912055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '785a6bdcf33d'
down_revision = 'dff8180648eb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('device_claims', sa.Column('provide_email', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_activated', sa.Boolean(), nullable=False, server_default="FALSE"))


def downgrade():
    op.drop_column('users', 'is_activated')
    op.drop_column('device_claims', 'provide_email')
