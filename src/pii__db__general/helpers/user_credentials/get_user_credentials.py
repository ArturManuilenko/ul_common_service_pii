from uuid import UUID
from typing import List

from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.pii__db__general.models.user_credentials import UserCredentials


def get_user_credentials_object(user_credentials_id: UUID) -> UserCredentials:
    user_credentials = UserCredentials.query.filter_by(id=user_credentials_id).first()
    return enshure_db_object_exists(UserCredentials, user_credentials)


def get_user_credentials_object_by_user(user_id: UUID) -> UserCredentials:
    user_credentials = UserCredentials.query.filter_by(user_id=user_id).first()
    return enshure_db_object_exists(UserCredentials, user_credentials)


def get_user_credentials_object_by_login(login: str) -> UserCredentials:
    user_credentials = UserCredentials.query.filter_by(login=login).first()
    return enshure_db_object_exists(UserCredentials, user_credentials)


def get_user_credentials_list(limit: int, offset: int) -> List[UserCredentials]:
    user_credentials_list = UserCredentials.query.offset(offset).limit(limit).all()
    return user_credentials_list
