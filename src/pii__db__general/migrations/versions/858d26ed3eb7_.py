"""empty message

Revision ID: 858d26ed3eb7
Revises: 4715520b5f1b
Create Date: 2021-07-27 06:02:58.709707

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from src.conf.permissions import permissions as permissions_registry
from src.conf.pii__db__general import PII__DB__GENERAL__SYS_USER_ID, PII__DB__GENERAL__GUEST_USER_ID, \
    PII__DB__GENERAL__ADMIN_USER_ID

# revision identifiers, used by Alembic.
revision = '858d26ed3eb7'
down_revision = '4715520b5f1b'
branch_labels = None
depends_on = None

ADMIN__LOGIN = 'lzkkQsLognjZ5TmifYiYdyi3Y4CcWH0W0KbrI7ES52o1p5M0ugoxMW6T2wySeeM2CYad18ztWBZtbCgAf2hBBw4MpHRw9IekbENdFDK1mdlHOVcVj1KzW85OQOJj77Ml42E4Qyy6TqinwJ4aBmbL4FdKsTlwqFJ12P51sbzHWxhOjlXemAgAVOqqtr7HBVdpUG4wAWDjjgjQDzMCXxSIgM4T9obzZXTa9FucUOuiNGwLOZEzkpRZOzRCMvomyB'
ADMIN__PASSWORD = 'UDM8B0hVFDuzdlO41PQLoXTpWusZur9GwBD8c11RL9GQcgO53CsHfI0H6Bj0MhunhgLz6aOfrZAYCmSmJrUYPa4eHSExcBA2fNycc300aGZU2JmUJhuFk3aXLwVgwrM48gAXTp5VkMGzQ3CiRScUYNhUZHsidYwuRNuiuJ3iIXoBZ3e1hHDLxTQdps4rVS8i9nelX9bub5IplJ9uctY6HNA52AiKTNFGpLW16gWUGzqD7bvXKycIZxyOuCdMdm'
ADMIN__PASSWORD_HASH = '$2b$12$9lxW5CTGERS/agRUeKYMKe5m1o20K7xHfB7ghL8KsOf.K7qouev2y'


def upgrade():
    # create root system user object
    dt_now = datetime.utcnow()
    op.execute("INSERT INTO public.user"
                "(id, user_created_id, user_modified_id, date_created, date_modified, is_alive, is_system) "
               f"VALUES ('{PII__DB__GENERAL__SYS_USER_ID}', '{PII__DB__GENERAL__SYS_USER_ID}',"
               f"'{PII__DB__GENERAL__SYS_USER_ID}', '{dt_now}', '{dt_now}', True, True)")

    op.execute("INSERT INTO public.user_data "
               "(id, email, admin_notes, user_created_id, user_modified_id, date_created, date_modified, is_alive) "
               f"VALUES ('{PII__DB__GENERAL__SYS_USER_ID}', 'root@root.root', 'root user', '{PII__DB__GENERAL__SYS_USER_ID}', "
               f"'{PII__DB__GENERAL__SYS_USER_ID}', '{dt_now}', '{dt_now}', True)")

    # create guest system user object
    op.execute("INSERT INTO public.user"
                "(id, user_created_id, user_modified_id, date_created, date_modified, is_alive, is_system) "
               f"VALUES ('{PII__DB__GENERAL__GUEST_USER_ID}', '{PII__DB__GENERAL__GUEST_USER_ID}',"
               f"'{PII__DB__GENERAL__GUEST_USER_ID}', '{dt_now}', '{dt_now}', True, True)")

    op.execute("INSERT INTO public.user_data "
               "(id, email, admin_notes, user_created_id, user_modified_id, date_created, date_modified, is_alive) "
               f"VALUES ('{PII__DB__GENERAL__GUEST_USER_ID}', 'guest@guest.guest', 'guest user', '{PII__DB__GENERAL__GUEST_USER_ID}', "
               f"'{PII__DB__GENERAL__GUEST_USER_ID}', '{dt_now}', '{dt_now}', True)")

    # create super admin user object
    op.execute("INSERT INTO public.user"
                "(id, user_created_id, user_modified_id, date_created, date_modified, is_alive, is_system) "
               f"VALUES ('{PII__DB__GENERAL__ADMIN_USER_ID}', '{PII__DB__GENERAL__ADMIN_USER_ID}',"
               f"'{PII__DB__GENERAL__ADMIN_USER_ID}', '{dt_now}', '{dt_now}', True, True)")

    op.execute("INSERT INTO public.user_data "
               "(id, email, admin_notes, user_created_id, user_modified_id, date_created, date_modified, is_alive) "
               f"VALUES ('{PII__DB__GENERAL__ADMIN_USER_ID}', 'superadmin@unic-lab.by', 'super admin user', '{PII__DB__GENERAL__ADMIN_USER_ID}', "
               f"'{PII__DB__GENERAL__ADMIN_USER_ID}', '{dt_now}', '{dt_now}', True)")

    op.execute("INSERT INTO public.user_credentials_request"
               "(id, user_created_id, user_modified_id, type, user_id, user_data_id, date_created, date_modified, is_alive) "
               f"VALUES ('{PII__DB__GENERAL__ADMIN_USER_ID}', '{PII__DB__GENERAL__ADMIN_USER_ID}', "
               f"'{PII__DB__GENERAL__ADMIN_USER_ID}', 'invite', '{PII__DB__GENERAL__ADMIN_USER_ID}', "
               f"'{PII__DB__GENERAL__ADMIN_USER_ID}', '{dt_now}', '{dt_now}', True)")

    op.execute("INSERT INTO public.user_credentials"
               "(id, user_created_id, user_modified_id, login, password, user_id, user_credentials_request_id, date_created, date_modified, is_alive) "
               f"VALUES ('{PII__DB__GENERAL__ADMIN_USER_ID}', '{PII__DB__GENERAL__ADMIN_USER_ID}', "
               f"'{PII__DB__GENERAL__ADMIN_USER_ID}', '{ADMIN__LOGIN}', '{ADMIN__PASSWORD_HASH}', "
               f"'{PII__DB__GENERAL__ADMIN_USER_ID}', '{PII__DB__GENERAL__ADMIN_USER_ID}', '{dt_now}', '{dt_now}', True)")

    op.add_column('user', sa.Column('user_data_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'user', 'user_data', ['user_data_id'], ['id'])

    op.execute(f"UPDATE public.user SET user_data_id = '{PII__DB__GENERAL__SYS_USER_ID}' "
               f"WHERE id = '{PII__DB__GENERAL__SYS_USER_ID}'")

    op.execute(f"UPDATE public.user SET user_data_id = '{PII__DB__GENERAL__GUEST_USER_ID}' "
               f"WHERE id = '{PII__DB__GENERAL__GUEST_USER_ID}'")

    op.execute(f"UPDATE public.user SET user_data_id = '{PII__DB__GENERAL__ADMIN_USER_ID}' "
               f"WHERE id = '{PII__DB__GENERAL__ADMIN_USER_ID}'")

    op.alter_column('user', 'user_data_id', nullable=False)

    # create super admin root organization
    all_permissions = permissions_registry.get_permissions_ids()
    all_permissions_list_str = ','.join([str(permission) for permission in all_permissions])
    op.execute("INSERT INTO public.organization_data "
               "(id, name, available_permissions, user_created_id, user_modified_id, date_created, date_modified, is_alive) "
               f"VALUES ('{PII__DB__GENERAL__ADMIN_USER_ID}', 'root', array[{all_permissions_list_str}], "
               f"'{PII__DB__GENERAL__SYS_USER_ID}', '{PII__DB__GENERAL__SYS_USER_ID}', '{dt_now}', '{dt_now}', True)")

    op.execute("INSERT INTO public.organization "
               "(id, admin_notes, organization_data_id, user_created_id, user_modified_id, date_created, date_modified, is_alive) "
               f"VALUES ('{PII__DB__GENERAL__ADMIN_USER_ID}', 'root', '{PII__DB__GENERAL__ADMIN_USER_ID}',"
               f"'{PII__DB__GENERAL__SYS_USER_ID}','{PII__DB__GENERAL__SYS_USER_ID}', '{dt_now}', '{dt_now}', True)")

    op.execute("INSERT INTO public.organization_team"
               "(id, name, organization_id, permissions, is_organization_admin, user_created_id, user_modified_id, date_created, date_modified, is_system, is_alive) "
               f"VALUES ('{PII__DB__GENERAL__ADMIN_USER_ID}', 'super admins', '{PII__DB__GENERAL__ADMIN_USER_ID}',"
               f"array[{all_permissions_list_str}], True, "
               f"'{PII__DB__GENERAL__SYS_USER_ID}','{PII__DB__GENERAL__SYS_USER_ID}', '{dt_now}', '{dt_now}', True, True)")

    op.execute("INSERT INTO public.organization_user"
               "(id, user_id, organization_id, state, notes, user_created_id, user_modified_id, date_created, date_modified, is_alive) "
               f"VALUES ('{PII__DB__GENERAL__ADMIN_USER_ID}', '{PII__DB__GENERAL__ADMIN_USER_ID}', '{PII__DB__GENERAL__ADMIN_USER_ID}',"
               f"'active', 'superadmin in superadmin organization', '{PII__DB__GENERAL__SYS_USER_ID}','{PII__DB__GENERAL__SYS_USER_ID}', '{dt_now}', '{dt_now}', True)")

    op.execute("INSERT INTO public.organization_team_user"
               "(id, user_id, organization_team_id, user_created_id, user_modified_id, date_created, date_modified, is_alive) "
               f"VALUES ('{PII__DB__GENERAL__ADMIN_USER_ID}', '{PII__DB__GENERAL__ADMIN_USER_ID}', '{PII__DB__GENERAL__ADMIN_USER_ID}',"
               f"'{PII__DB__GENERAL__SYS_USER_ID}','{PII__DB__GENERAL__SYS_USER_ID}', '{dt_now}', '{dt_now}', True)")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'user_data_id')
    op.drop_column('organization', 'organization_data_id')
    # ### end Alembic commands ###
