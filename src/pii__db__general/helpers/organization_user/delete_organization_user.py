from uuid import UUID

from db_utils.utils.query_soft_delete import query_soft_delete
from src.pii__db__general.models.organization_user import OrganizationUser


def delete_organization_user(organization_user_id: UUID, user_deleted_id: UUID) -> None:
    query_soft_delete(OrganizationUser, organization_user_id, user_deleted_id)
