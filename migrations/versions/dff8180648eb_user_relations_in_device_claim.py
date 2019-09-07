"""user relations in device_claim

Revision ID: dff8180648eb
Revises: 4d0238d04c7e
Create Date: 2019-09-07 12:29:02.440278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dff8180648eb'
down_revision = '4d0238d04c7e'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("device_claims") as batch_op:
        batch_op.add_column(sa.Column('admin_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('admin_message', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('admin_timestamp', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('claim_message', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('claim_timestamp', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('claimer_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('device_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('owner_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('owner_message', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('owner_timestamp', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key('fk_device_claims_devices', 'devices', ['device_id'], ['id'])
        batch_op.create_foreign_key('fk_device_claims_users_owner', 'users', ['owner_id'], ['id'])
        batch_op.create_foreign_key('fk_device_claims_users_claimer', 'users', ['claimer_id'], ['id'])
        batch_op.create_foreign_key('fk_device_claims_users_admin', 'users', ['admin_id'], ['id'])
        batch_op.drop_column('respond_timestamp')
        batch_op.drop_column('respond_message')
        batch_op.drop_column('request_timestamp')
        batch_op.drop_column('request_message')


def downgrade():
    with op.batch_alter_table("device_claims") as batch_op:
        batch_op.add_column(sa.Column('request_message', sa.VARCHAR(length=255), nullable=False))
        batch_op.add_column(sa.Column('request_timestamp', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('respond_message', sa.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('respond_timestamp', sa.DATETIME(), nullable=True))
        batch_op.drop_constraint('fk_device_claims_devices', type_='foreignkey')
        batch_op.drop_constraint('fk_device_claims_users_owner', type_='foreignkey')
        batch_op.drop_constraint('fk_device_claims_users_claimer', type_='foreignkey')
        batch_op.drop_constraint('fk_device_claims_users_admin', type_='foreignkey')
        batch_op.drop_column('owner_timestamp')
        batch_op.drop_column('owner_message')
        batch_op.drop_column('owner_id')
        batch_op.drop_column('device_id')
        batch_op.drop_column('claimer_id')
        batch_op.drop_column('claim_timestamp')
        batch_op.drop_column('claim_message')
        batch_op.drop_column('admin_timestamp')
        batch_op.drop_column('admin_message')
        batch_op.drop_column('admin_id')
