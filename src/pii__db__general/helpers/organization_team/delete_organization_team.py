from uuid import UUID

from db_utils.utils.query_soft_delete import query_soft_delete
from src.pii__db__general.models.organization_team import OrganizationTeam


def delete_organization_team(
    organization_team_id: UUID,
    user_deleted_id: UUID
) -> None:
    query_soft_delete(OrganizationTeam, organization_team_id, user_deleted_id)
