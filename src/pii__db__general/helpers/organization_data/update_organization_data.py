from uuid import UUID

from src.pii__db__general.models.organization_data import OrganizationData
from src.pii__db__general.helpers.organization_data.get_organization_data import \
    get_organization_data_object


def update_organization_data_obj(
    organization_data_id: UUID,
    name: str,
    user_modified_id: UUID,
) -> OrganizationData:
    organization_data_obj = get_organization_data_object(organization_data_id)
    organization_data_obj.name = name
    organization_data_obj.mark_as_modified(user_modified_id)
    return organization_data_obj
