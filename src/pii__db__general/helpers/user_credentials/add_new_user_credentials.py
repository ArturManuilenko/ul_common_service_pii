from datetime import datetime
from typing import Optional
from uuid import uuid4

from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql.base import UUID
from src.pii__db__general.models.user_credentials import UserCredentials


def add_new_user_credentials(
    login: str,
    password: str,
    date_expiration: Optional[datetime],
    user_credentials_request_id: UUID,
    user_id: UUID,
    user_created_id: UUID,
) -> UserCredentials:

    new_user_credenetials = UserCredentials(
        id=uuid4(),
        login=login,
        password=password,
        date_expiration=date_expiration,
        user_credentials_request_id=user_credentials_request_id,
        user_id=user_id,
    )
    new_user_credenetials.mark_as_created(user_created_id)
    db.session.add(new_user_credenetials)

    return new_user_credenetials
