from typing import List
from uuid import UUID, uuid4

from db_utils.modules.db import db
from src.pii__db__general.models.organization_data import OrganizationData


def add_new_organization_data(
    name: str,
    available_permissions: List[int],
    user_created_id: UUID
) -> OrganizationData:
    new_organization_data = OrganizationData(
        id=uuid4(),
        name=name,
        available_permissions=available_permissions,
    )
    new_organization_data.mark_as_created(user_created_id)
    db.session.add(new_organization_data)
    return new_organization_data
