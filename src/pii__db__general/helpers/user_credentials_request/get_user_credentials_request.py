from typing import List
from uuid import UUID

from src.pii__db__general.models.user_credentials_request import UserCredentialsRequest, UserCredentialsRequestType
from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists


def get_user_credentials_request_object(type: UserCredentialsRequestType, user_credentials_request_id: UUID) -> UserCredentialsRequest:
    user_credentials_request = UserCredentialsRequest.query\
        .filter_by(type=type)\
        .filter_by(id=user_credentials_request_id)\
        .first()
    return enshure_db_object_exists(UserCredentialsRequest, user_credentials_request)


def get_user_credentials_request_list(
    type: UserCredentialsRequestType,
    limit: int,
    offset: int
) -> List[UserCredentialsRequest]:
    user_credentials_request = UserCredentialsRequest.query\
        .filter_by(type=type)\
        .limit(limit)\
        .offset(offset)\
        .all()
    return user_credentials_request


def get_user_credentials_request_list_by_org(
    type: UserCredentialsRequestType,
    limit: int,
    offset: int,
    organization_id: UUID,
) -> List[UserCredentialsRequest]:
    user_credentials_request = UserCredentialsRequest.query\
        .filter_by(type=type)\
        .filter_by(organization_id=organization_id)\
        .limit(limit)\
        .offset(offset)\
        .all()
    return user_credentials_request


def get_credentials_request_total_count() -> int:
    return UserCredentialsRequest.query.count()


def get_credentials_request_by_org_total_count(organization_id: UUID) -> int:
    return UserCredentialsRequest.query.filter_by(organization_id=organization_id).count()
