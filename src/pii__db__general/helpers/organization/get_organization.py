from typing import List
from uuid import UUID

from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.pii__db__general.models.organization_team_user import OrganizationTeamUser
from src.pii__db__general.models.organization_team import OrganizationTeam
from src.pii__db__general.models.organization import Organization


def get_organization_object(organization_id: UUID) -> Organization:
    organization = Organization.query\
        .filter_by(id=organization_id)\
        .first()
    return enshure_db_object_exists(Organization, organization)


def get_organization_list(limit: int, offset: int) -> List[Organization]:
    organization_list = Organization.query\
        .offset(offset)\
        .limit(limit)\
        .all()
    return organization_list


def get_organization_total_count() -> int:
    return Organization.query.count()


def get_first_user_organization(user_id: UUID) -> Organization:
    first_user_organization_team_user = OrganizationTeamUser.query.filter_by(user_id=user_id).first()
    first_user_organization_team = OrganizationTeam.query.filter_by(
        id=first_user_organization_team_user.organization_team_id
    ).first()
    first_user_organization = first_user_organization_team.organization
    return first_user_organization


def get_user_organizations(user_id: UUID, limit: int, offset: int) -> List[Organization]:
    user_org_list = Organization.query\
        .join(OrganizationTeam) \
        .join(OrganizationTeamUser)\
        .filter(OrganizationTeamUser.user_id == user_id) \
        .offset(offset).limit(limit).all()
    return user_org_list


def get_user_organizations_count(user_id: UUID) -> int:
    user_org_list_count = Organization.query\
        .join(OrganizationTeam) \
        .join(OrganizationTeamUser)\
        .filter(OrganizationTeamUser.user_id == user_id)\
        .count()
    return user_org_list_count
