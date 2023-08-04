from typing import List
from uuid import UUID, uuid4

from db_utils.modules.db import db
from src.pii__db__general.models.organization_team import OrganizationTeam


def add_new_organization_team(
    name: str,
    permissions: List[int],
    is_organization_admin: bool,
    user_created_id: UUID,
    organization_id: UUID,
    is_system: bool = False
) -> OrganizationTeam:

    new_organization_team = OrganizationTeam(
        id=uuid4(),
        name=name,
        permissions=permissions,
        is_organization_admin=is_organization_admin,
        organization_id=organization_id,
        is_system=is_system,
    )
    new_organization_team.mark_as_created(user_created_id)
    db.session.add(new_organization_team)

    return new_organization_team
