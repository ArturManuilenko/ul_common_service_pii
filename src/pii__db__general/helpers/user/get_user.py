from uuid import UUID
from typing import List, Set

from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.pii__db__general.helpers.organization.get_organization import get_organization_object
from src.pii__db__general.models.organization_team_user import OrganizationTeamUser
from src.pii__db__general.models.organization_team import OrganizationTeam
from src.pii__db__general.models.user import User


def get_user_object(user_id: UUID) -> User:
    user = User.query.filter_by(id=user_id).first()
    return enshure_db_object_exists(User, user)


def get_user_list(limit: int, offset: int) -> List[User]:
    user_list = User.query.offset(offset).limit(limit).all()
    return user_list


def get_user_total_count() -> int:
    return User.query.count()


def get_user_permissions_by_organization(user_id: UUID, organization_id: UUID) -> Set[int]:
    """Util for get all user teams permissions"""
    user_organization_teams = OrganizationTeam.query \
        .join(OrganizationTeamUser) \
        .filter(OrganizationTeamUser.user_id == user_id)\
        .filter(OrganizationTeam.organization_id == organization_id)\
        .all()

    user_organization_teams_permissions = set(permission for user_org_team in user_organization_teams for permission in user_org_team.permissions)
    user_organization_permissions = set(get_organization_object(organization_id).organization_data.available_permissions)
    user_permissions = user_organization_teams_permissions & user_organization_permissions
    return user_permissions


def get_organization_user(organization_id: UUID, user_id: UUID) -> User:
    user = User.query\
        .join(OrganizationTeamUser, OrganizationTeamUser.user_id == user_id) \
        .join(OrganizationTeam)\
        .filter(OrganizationTeamUser.organization_team_id == OrganizationTeam.id) \
        .filter(OrganizationTeam.organization_id == organization_id)\
        .first()
    return enshure_db_object_exists(user)


def get_organization_users(organization_id: UUID, limit: int, offset: int) -> List[User]:
    user_list_by_org = User.query \
        .join(OrganizationTeamUser, OrganizationTeamUser.user_id == User.id) \
        .join(OrganizationTeam)\
        .filter(OrganizationTeamUser.organization_team_id == OrganizationTeam.id) \
        .filter(OrganizationTeam.organization_id == organization_id) \
        .offset(offset)\
        .limit(limit) \
        .all()
    return user_list_by_org


def get_organization_users_count(organization_id: UUID) -> int:
    organization_team_user_list_count = OrganizationTeamUser.query\
        .join(OrganizationTeam)\
        .filter(OrganizationTeam.organization_id == organization_id)\
        .count()
    return organization_team_user_list_count


def get_organization_team_users(
    organization_id: UUID,
    organization_team_id: UUID,
    limit: int,
    offset: int
) -> List[User]:
    organization_team_user_list = User.query\
        .join(OrganizationTeamUser, User.id == OrganizationTeamUser.user_id)\
        .join(OrganizationTeam, OrganizationTeamUser.organization_team_id == OrganizationTeam.id)\
        .filter(OrganizationTeam.organization_id == organization_id)\
        .filter(OrganizationTeamUser.organization_team_id == organization_team_id)\
        .limit(limit)\
        .offset(offset)\
        .all()
    return organization_team_user_list


def get_organization_team_users_count(
    organization_id: UUID,
    organization_team_id: UUID
) -> int:
    organization_team_user_list_count = OrganizationTeamUser.query\
        .join(OrganizationTeam)\
        .filter(OrganizationTeam.organization_id == organization_id)\
        .filter(OrganizationTeamUser.organization_team_id == organization_team_id)\
        .count()
    return organization_team_user_list_count
