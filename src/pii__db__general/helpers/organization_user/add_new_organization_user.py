from uuid import UUID, uuid4

from db_utils.modules.db import db
from src.pii__db__general.models.organization_user import OrganizationUser, OrganizationUserState


def add_new_organization_user(
    notes: str,
    state: OrganizationUserState,
    user_created_id: UUID,
    organization_id: UUID,
    user_id: UUID,
) -> OrganizationUser:
    new_organization_user = OrganizationUser.query.with_deleted()\
        .filter_by(organization_id=organization_id)\
        .filter_by(user_id=user_id)\
        .first()
    if new_organization_user:
        if new_organization_user.is_alive:
            return new_organization_user
        new_organization_user.is_alive = True
        new_organization_user.date_deleted = None
        new_organization_user.user_deleted = None
        new_organization_user.mark_as_created(user_created_id)
        return new_organization_user
    new_organization_user = OrganizationUser(
        id=uuid4(),
        notes=notes,
        state=state,
        organization_id=organization_id,
        user_id=user_id,
    )
    new_organization_user.mark_as_created(user_created_id)
    db.session.add(new_organization_user)
    return new_organization_user
