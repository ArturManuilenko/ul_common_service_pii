from typing import Optional
from uuid import uuid4

from db_utils.modules.db import db
from api_utils.errors.object_has_already_exists_error import ObjectHasAlreadyExistsError
from sqlalchemy.dialects.postgresql.base import UUID
from src.pii__db__general.models.user_data import UserData


def add_new_user_data(
    email: str,
    nick_name: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
    middle_name: Optional[str],
    avatar_media_file_id: Optional[UUID],
    about: Optional[str],
    admin_notes: Optional[str],
    user_created_id: UUID,
) -> UserData:

    # check user_data email uniq
    if user_data := UserData.query.filter_by(email=email).first():
        raise ObjectHasAlreadyExistsError(f"UserData {user_data.id} already exist")

    new_user_data = UserData(
        id=uuid4(),
        email=email,
        nick_name=nick_name,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        avatar_media_file_id=avatar_media_file_id,
        about=about,
        admin_notes=admin_notes,
    )
    new_user_data.mark_as_created(user_created_id)
    db.session.add(new_user_data)
    return new_user_data
