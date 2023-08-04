from uuid import UUID

from src.pii__db__general.models.organization_data import OrganizationData
from src.pii__db__general.models.organization import Organization
from db_utils.utils.query_soft_delete import query_soft_delete


def delete_organization(organization_id: UUID, user_deleted_id: UUID) -> None:
    organization = query_soft_delete(Organization, organization_id, user_deleted_id)
    query_soft_delete(OrganizationData, organization.organization_data_id, user_deleted_id)
