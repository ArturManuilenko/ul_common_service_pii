from uuid import UUID

from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.pii__db__general.models.organization_user import OrganizationUser


def get_organization_user_object_by_id(organization_user_id: UUID) -> OrganizationUser:
    organization_user = OrganizationUser.query.filter_by(id=organization_user_id).first()
    return enshure_db_object_exists(OrganizationUser, organization_user)


def get_organization_user_object(organization_id: UUID, user_id: UUID) -> OrganizationUser:
    organization_user = OrganizationUser.query\
        .filter_by(organization_id=organization_id)\
        .filter_by(user_id_id=user_id)\
        .first()
    return enshure_db_object_exists(OrganizationUser, organization_user)
