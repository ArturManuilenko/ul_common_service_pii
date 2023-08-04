from uuid import UUID, uuid4

from db_utils.modules.db import db
from src.conf.permissions import permissions
from src.conf.permissions import DEFAULT_ORGANIZATION_AVAILABLE_PERMISSION_LIST
from src.pii__db__general.models.organization import Organization
from src.pii__db__general.helpers.organization_data.add_new_organization_data import \
    add_new_organization_data


def add_new_organization(
        admin_notes: str,
        name: str,
        user_created_id: UUID,
) -> Organization:
    new_organization_data = add_new_organization_data(
        name=name,
        available_permissions=permissions.get_ids_from_iterable(DEFAULT_ORGANIZATION_AVAILABLE_PERMISSION_LIST),
        user_created_id=user_created_id,
    )
    new_organization = Organization(
        id=uuid4(),
        organization_data_id=new_organization_data.id,
        admin_notes=admin_notes,
    )
    new_organization.mark_as_created(user_created_id)
    db.session.add(new_organization)
    return new_organization
