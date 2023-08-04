from uuid import UUID

from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.pii__db__general.models.organization_team_user import OrganizationTeamUser


def get_organization_team_user_object(organization_team_user_id: UUID) -> OrganizationTeamUser:
    organization_team_user = OrganizationTeamUser.query.filter_by(id=organization_team_user_id).first()
    return enshure_db_object_exists(OrganizationTeamUser, organization_team_user)
