from uuid import UUID

from db_utils.utils.query_soft_delete import query_soft_delete
from src.pii__db__general.models.organization_team_user import OrganizationTeamUser


def delete_organization_team_user(organization_team_user_id: UUID, user_deleted_id: UUID) -> None:
    query_soft_delete(OrganizationTeamUser, organization_team_user_id, user_deleted_id)
