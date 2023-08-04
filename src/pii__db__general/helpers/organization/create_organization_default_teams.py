from uuid import UUID

from src.pii__db__general.helpers.organization_team.add_new_organization_team import \
    add_new_organization_team
from src.conf.permissions import permissions
from src.conf.permissions import DEFAULT_ORGANIZATION_AVAILABLE_PERMISSION_LIST
from src.conf.pii__api__general import \
    ORGANIZATION_DEFAULT_INACTIVE_TEAM_NAME, \
    ORGANIZATION_DEFAULT_USERS_TEAM_NAME, \
    ORGANIZATION_DEFAULT_ADMIN_TEAM_NAME


def create_organization_default_teams(
    organization_id: UUID,
    user_created_id: UUID,
) -> None:
    # create default admin team
    add_new_organization_team(
        name=ORGANIZATION_DEFAULT_ADMIN_TEAM_NAME,
        permissions=permissions.get_ids_from_iterable(DEFAULT_ORGANIZATION_AVAILABLE_PERMISSION_LIST),
        user_created_id=user_created_id,
        organization_id=organization_id,
        is_organization_admin=True,
        is_system=True
    )
    # create default users team
    add_new_organization_team(
        name=ORGANIZATION_DEFAULT_USERS_TEAM_NAME,
        permissions=[],
        user_created_id=user_created_id,
        organization_id=organization_id,
        is_organization_admin=False,
        is_system=True
    )
    # create default inactive users team
    add_new_organization_team(
        name=ORGANIZATION_DEFAULT_INACTIVE_TEAM_NAME,
        permissions=[],
        user_created_id=user_created_id,
        organization_id=organization_id,
        is_organization_admin=False,
        is_system=True
    )
