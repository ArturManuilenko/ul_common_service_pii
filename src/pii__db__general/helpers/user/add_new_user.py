from typing import Optional
from uuid import uuid4

from sqlalchemy.dialects.postgresql.base import UUID
from db_utils.modules.db import db
from src.pii__db__general.models.user import User
from src.pii__db__general.helpers.user_data.add_new_user_data import add_new_user_data


def add_new_user(
    email: str,
    nick_name: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
    middle_name: Optional[str],
    avatar_media_file_id: Optional[UUID],
    about: Optional[str],
    admin_notes: Optional[str],
    user_created_id: UUID,
) -> User:
    new_user_data = add_new_user_data(
        email=email,
        nick_name=nick_name,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        avatar_media_file_id=avatar_media_file_id,
        about=about,
        admin_notes=admin_notes,
        user_created_id=user_created_id,
    )
    new_user = User(
        id=uuid4(),
        user_data_id=new_user_data.id,
    )
    new_user.mark_as_created(user_created_id)
    db.session.add(new_user)

    return new_user


def add_new_user_with_existing_data(
    user_data_id: UUID,
    user_created_id: UUID,
) -> User:
    new_user = User(
        id=uuid4(),
        user_data_id=user_data_id,
    )
    new_user.mark_as_created(user_created_id)
    db.session.add(new_user)
    return new_user
