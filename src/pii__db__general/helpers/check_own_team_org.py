from uuid import UUID

from api_utils.errors.api_no_result_found import ApiNoResultFoundError
from src.pii__db__general.models.organization_team import OrganizationTeam


def check_own_team_org(
    organization_id: UUID,
    organization_team_id: UUID
) -> None:
    """ Util for check own db instances:
    Team -> Organization """
    org_team = OrganizationTeam.query.filter_by(
        organization_id=organization_id,
        id=organization_team_id,
    ).first()
    if not org_team:
        raise ApiNoResultFoundError(f"OrganizationTeam {organization_team_id} in Organization {organization_id} not found")
    if org_team.organization.id != organization_id:
        raise ApiNoResultFoundError(f"Organization {organization_id} not has OrganizationTeam {organization_team_id}")
