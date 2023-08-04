
from uuid import UUID, uuid4

from db_utils.modules.db import db
from src.pii__db__general.models.organization_team_user import OrganizationTeamUser
from src.pii__db__general.helpers.check_own_team_org import check_own_team_org
from src.pii__db__general.models.user import User


def add_user_to_org_team(
    user_id: UUID,
    organization_id: UUID,
    organization_team_id: UUID,
    user_created_id: UUID,
) -> User:
    check_own_team_org(
        organization_id=organization_id,
        organization_team_id=organization_team_id
    )
    new_organization_team_user = OrganizationTeamUser.query.with_deleted()\
        .filter_by(user_id=user_id) \
        .filter_by(organization_team_id=organization_team_id) \
        .first()
    if new_organization_team_user:
        if new_organization_team_user.is_alive:
            return new_organization_team_user
        new_organization_team_user.is_alive = True
        new_organization_team_user.date_deleted = None
        new_organization_team_user.user_deleted = None
        new_organization_team_user.mark_as_created(user_created_id)
        return new_organization_team_user
    new_organization_team_user = OrganizationTeamUser(
        id=uuid4(),
        user_id=user_id,
        organization_team_id=organization_team_id,
    )
    new_organization_team_user.mark_as_created(user_created_id)
    db.session.add(new_organization_team_user)
    return new_organization_team_user
