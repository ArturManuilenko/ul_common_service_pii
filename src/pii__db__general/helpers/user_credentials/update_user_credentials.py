from uuid import UUID
from datetime import datetime
from typing import Optional
from src.pii__db__general.models.user_credentials import UserCredentials
from src.pii__db__general.helpers.user_credentials.get_user_credentials import get_user_credentials_object


def update_user_credentials_obj(
    user_credentials_id: UUID,
    login: str,
    password: str,
    date_expiration: Optional[datetime],
    user_modified_id: UUID,
) -> UserCredentials:
    user_credentials_obj = get_user_credentials_object(user_credentials_id)
    user_credentials_obj.login = login
    user_credentials_obj.password = password
    user_credentials_obj.date_expiration = date_expiration if date_expiration else user_credentials_obj.date_expiration
    user_credentials_obj.mark_as_modified(user_modified_id)
    return user_credentials_obj
