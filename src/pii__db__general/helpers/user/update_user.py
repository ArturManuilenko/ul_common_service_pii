from uuid import UUID
from typing import Optional

from src.pii__db__general.models.user import User
from src.pii__db__general.helpers.user.get_user import get_user_object
from src.pii__db__general.helpers.user_data.update_user_data import update_user_data_obj


def update_user(
    user_id: UUID,
    user_modified_id: UUID,
    email: str,
    nick_name: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
    middle_name: Optional[str],
    avatar_media_file_id: Optional[UUID],
    about: Optional[str],
    admin_notes: Optional[str],
) -> User:
    user_obj = get_user_object(user_id)
    user_data = update_user_data_obj(
        user_data_id=user_obj.user_data_id,
        email=email,
        nick_name=nick_name,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        avatar_media_file_id=avatar_media_file_id,
        about=about,
        admin_notes=admin_notes,
        user_modified_id=user_modified_id,
    )
    user_data.mark_as_modified(user_modified_id)
    return user_obj
