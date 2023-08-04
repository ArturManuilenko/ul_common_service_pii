from uuid import UUID
from typing import List

from src.pii__db__general.models.organization_team import OrganizationTeam
from src.pii__db__general.helpers.organization_team.get_organization_team import \
    get_organization_team_object


def update_organization_team_obj(
    organization_id: UUID,
    organization_team_id: UUID,
    name: str,
    permissions: List[int],
    is_organization_admin: bool,
    user_modified_id: UUID,
) -> OrganizationTeam:
    organization_team_obj = get_organization_team_object(
        organizaton_id=organization_id,
        organization_team_id=organization_team_id
    )
    organization_team_obj.name = name
    organization_team_obj.permissions = permissions
    organization_team_obj.is_organization_admin = is_organization_admin
    organization_team_obj.mark_as_modified(user_modified_id)
    return organization_team_obj
