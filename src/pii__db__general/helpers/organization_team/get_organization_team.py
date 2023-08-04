from src.pii__db__general.models.organization_team_user import OrganizationTeamUser
from src.pii__db__general.helpers.user.get_user import get_user_object
from typing import List
from uuid import UUID

from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.pii__db__general.helpers.organization.get_organization import get_organization_object
from src.pii__db__general.models.organization_team import OrganizationTeam


def get_organization_team_object(organization_id: UUID, organization_team_id: UUID) -> OrganizationTeam:
    organization_team = OrganizationTeam.query.filter_by(
        organization_id=organization_id,
        id=organization_team_id,
    ).first()
    return enshure_db_object_exists(OrganizationTeam, organization_team)


def get_organization_teams(organization_id: UUID, limit: int, offset: int) -> List[OrganizationTeam]:
    get_organization_object(organization_id)
    organization_team_list_by_org = OrganizationTeam.query\
        .filter_by(organization_id=organization_id) \
        .offset(offset) \
        .limit(limit) \
        .all()
    return organization_team_list_by_org


def get_organization_teams_count(organization_id: UUID) -> int:
    organization_team_list_by_org_count = OrganizationTeam.query\
        .filter_by(organization_id=organization_id) \
        .count()
    return organization_team_list_by_org_count


def get_user_organization_teams(user_id: UUID, limit: int, offset: int) -> List[OrganizationTeam]:
    get_user_object(user_id)
    user_org_teams_list = OrganizationTeam.query \
        .join(OrganizationTeamUser) \
        .filter(OrganizationTeamUser.user_id == user_id) \
        .filter(OrganizationTeam.id == OrganizationTeamUser.organization_team_id) \
        .offset(offset)\
        .limit(limit)\
        .all()
    return user_org_teams_list


def get_user_organization_teams_count(user_id: UUID) -> List[OrganizationTeam]:
    get_user_object(user_id)
    user_org_teams_list = OrganizationTeam.query \
        .join(OrganizationTeamUser) \
        .filter(OrganizationTeamUser.user_id == user_id) \
        .filter(OrganizationTeam.id == OrganizationTeamUser.organization_team_id) \
        .count()
    return user_org_teams_list
