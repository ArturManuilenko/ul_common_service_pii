from typing import List
from uuid import UUID

from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.pii__db__general.models.organization_data import OrganizationData


def get_organization_data_object(organization_data_id: UUID) -> OrganizationData:
    organization_data = OrganizationData.query.filter_by(id=organization_data_id).first()
    return enshure_db_object_exists(OrganizationData, organization_data)


def get_organization_data_list(limit: int, offset: int) -> List[OrganizationData]:
    organization_data_list = OrganizationData.query.offset(offset).limit(limit).all()
    return organization_data_list


def get_organization_data_total_count() -> int:
    return OrganizationData.query.count()
