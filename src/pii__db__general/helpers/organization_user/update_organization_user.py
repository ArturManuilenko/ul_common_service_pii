from uuid import UUID

from src.pii__db__general.models.organization_user import OrganizationUser, OrganizationUserState
from src.pii__db__general.helpers.organization_user.get_organization_user import \
    get_organization_user_object, get_organization_user_object_by_id


def update_organization_user_obj_by_id(
        organization_user_id: UUID,
        notes: str,
        state: OrganizationUserState,
        user_modified_id: UUID,
) -> OrganizationUser:
    organization_user_obj = get_organization_user_object_by_id(
        organization_user_id=organization_user_id
    )
    organization_user_obj.notes = notes
    organization_user_obj.state = state
    organization_user_obj.mark_as_modified(user_modified_id)
    return organization_user_obj


def update_organization_user_obj(
        organization_id: UUID,
        user_id: UUID,
        notes: str,
        state: OrganizationUserState,
        user_modified_id: UUID,
) -> OrganizationUser:
    organization_user_obj = get_organization_user_object(organization_id=organization_id, user_id=user_id)
    organization_user_obj.notes = notes
    organization_user_obj.state = state
    organization_user_obj.mark_as_modified(user_modified_id)
    return organization_user_obj
