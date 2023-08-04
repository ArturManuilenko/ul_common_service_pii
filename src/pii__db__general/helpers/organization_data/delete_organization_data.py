from uuid import UUID

from db_utils.utils.query_soft_delete import query_soft_delete
from src.pii__db__general.models.organization_data import OrganizationData


def delete_organization_data(organization_data_id: UUID, user_deleted_id: UUID) -> None:
    query_soft_delete(OrganizationData, organization_data_id, user_deleted_id)
