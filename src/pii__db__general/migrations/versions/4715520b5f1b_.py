"""empty message

Revision ID: 4715520b5f1b
Revises: 
Create Date: 2021-07-27 06:00:58.368828

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from src.pii__db__general.modules.hashed_field import BHashedBinary

# revision identifiers, used by Alembic.
revision = '4715520b5f1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('date_deleted', sa.DateTime(), nullable=True),
    sa.Column('is_alive', sa.Boolean(), nullable=False),
    sa.Column('is_system', sa.Boolean(), nullable=False),
    sa.Column('user_created_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_modified_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_deleted_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_created_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_deleted_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_modified_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_auth_log',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('user_created_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('type', sa.Enum('login', 'refresh_auth', name='userauthlogtype'), nullable=False),
    sa.Column('user_agent', sa.String(length=1000), nullable=True),
    sa.Column('ipv4', sa.String(length=15), nullable=True),
    sa.ForeignKeyConstraint(['user_created_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_data',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('date_deleted', sa.DateTime(), nullable=True),
    sa.Column('is_alive', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('available_permissions', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('user_created_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_modified_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_deleted_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_created_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_deleted_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_modified_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_data',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('date_deleted', sa.DateTime(), nullable=True),
    sa.Column('is_alive', sa.Boolean(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('nick_name', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('middle_name', sa.String(length=255), nullable=True),
    sa.Column('avatar_media_file_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('admin_notes', sa.String(length=1000), nullable=True),
    sa.Column('about', sa.String(length=1000), nullable=True),
    sa.Column('user_created_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_modified_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_deleted_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_created_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_deleted_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_modified_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('date_deleted', sa.DateTime(), nullable=True),
    sa.Column('is_alive', sa.Boolean(), nullable=False),
    sa.Column('admin_notes', sa.String(length=2000), nullable=True),
    sa.Column('organization_data_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_created_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_modified_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_deleted_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['organization_data_id'], ['organization_data.id'], ),
    sa.ForeignKeyConstraint(['user_created_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_deleted_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_modified_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('date_deleted', sa.DateTime(), nullable=True),
    sa.Column('is_alive', sa.Boolean(), nullable=False),
    sa.Column('notes', sa.String(length=1000), nullable=False),
    sa.Column('state', sa.Enum('active', 'blocked', name='organizationuserstate'), nullable=False),
    sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_created_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_modified_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_deleted_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['user_created_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_deleted_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_modified_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_team',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('date_deleted', sa.DateTime(), nullable=True),
    sa.Column('is_alive', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('permissions', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('is_organization_admin', sa.Boolean(), nullable=False),
    sa.Column('is_system', sa.Boolean(), nullable=False),
    sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_created_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_modified_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_deleted_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['user_created_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_deleted_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_modified_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_team_user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('date_deleted', sa.DateTime(), nullable=True),
    sa.Column('is_alive', sa.Boolean(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('organization_team_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_created_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_modified_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_deleted_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['organization_team_id'], ['organization_team.id'], ),
    sa.ForeignKeyConstraint(['user_created_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_deleted_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_modified_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_credentials_request',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('date_deleted', sa.DateTime(), nullable=True),
    sa.Column('is_alive', sa.Boolean(), nullable=False),
    sa.Column('date_confirmed', sa.DateTime(), nullable=True),
    sa.Column('type', sa.Enum('invite', 'reset_password', 'change_password', name='usercredentialsrequesttype'), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_data_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('organization_team_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_created_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_modified_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_deleted_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['organization_team_id'], ['organization_team.id'], ),
    sa.ForeignKeyConstraint(['user_created_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_data_id'], ['user_data.id'], ),
    sa.ForeignKeyConstraint(['user_deleted_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_modified_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    )
    op.create_table('user_credentials',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.Column('date_deleted', sa.DateTime(), nullable=True),
    sa.Column('is_alive', sa.Boolean(), nullable=False),
    sa.Column('login', sa.String(length=255), nullable=False),
    sa.Column('password', BHashedBinary(), nullable=False),
    sa.Column('date_expiration', sa.DateTime(), nullable=True),
    sa.Column('user_credentials_request_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_created_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_modified_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_deleted_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_created_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_credentials_request_id'], ['user_credentials_request.id'], ),
    sa.ForeignKeyConstraint(['user_deleted_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_modified_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_credentials')
    op.drop_table('user_credentials_request')
    op.drop_table('organization_team_user')
    op.drop_table('organization_team')
    op.drop_table('organization_user')
    op.drop_table('organization')
    op.drop_table('user_data')
    op.drop_table('organization_data')
    op.drop_table('user_auth_log')
    op.drop_table('user')
    op.execute("DROP TYPE usercredentialsrequesttype")
    op.execute("DROP TYPE userauthlogtype")
    op.execute("DROP TYPE organizationuserstate")
    # ### end Alembic commands ###