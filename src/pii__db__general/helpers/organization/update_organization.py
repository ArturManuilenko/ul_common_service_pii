from uuid import UUID

from src.pii__db__general.helpers.organization.get_organization import get_organization_object
from src.pii__db__general.helpers.organization_data.update_organization_data import \
    update_organization_data_obj
from src.pii__db__general.models.organization import Organization


def update_organization(
    organization_id: UUID,
    name: str,
    admin_notes: str,
    user_modified_id: UUID,
) -> Organization:
    organization_obj = get_organization_object(organization_id)
    organization_obj.admin_notes = admin_notes
    organization_obj.mark_as_modified(user_modified_id)

    update_organization_data_obj(
        organization_data_id=organization_obj.organization_data_id,
        name=name,
        user_modified_id=user_modified_id,
    )
    return organization_obj
