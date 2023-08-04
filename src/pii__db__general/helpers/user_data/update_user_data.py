from uuid import UUID
from typing import Optional
from api_utils.errors.api_validate_error import ApiValidateError
from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.pii__db__general.models.user_data import UserData
from src.pii__db__general.helpers.user_data.get_user_data import get_user_data_object
from src.pii__db__general.models.user import User
from src.pii__db__general.helpers.user.get_user import get_user_object


def update_user_data_obj(
    user_data_id: UUID,
    user_modified_id: UUID,
    email: str,
    nick_name: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
    middle_name: Optional[str],
    avatar_media_file_id: Optional[UUID],
    about: Optional[str],
    admin_notes: Optional[str]
) -> UserData:

    user_data_obj = get_user_data_object(user_data_id)
    enshure_db_object_exists(UserData, user_data_obj)

    # check user_data email unique
    user_data_duplicate = UserData.query.filter_by(email=email).first()
    if user_data_duplicate and user_data_duplicate.id != user_data_obj.id:
        raise ApiValidateError(
            code="not_unique",
            msg_template="email is not unique",
            location="email",
        )

    user_data_obj.email = email
    user_data_obj.nick_name = nick_name
    user_data_obj.first_name = first_name
    user_data_obj.last_name = last_name
    user_data_obj.middle_name = middle_name
    user_data_obj.avatar_media_file_id = avatar_media_file_id
    user_data_obj.about = about
    user_data_obj.admin_notes = admin_notes
    user_data_obj.mark_as_modified(user_modified_id)

    return user_data_obj


def update_current_user_data_obj(
    user_id: UUID,
    user_modified_id: UUID,
    email: str,
    nick_name: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
    middle_name: Optional[str],
    avatar_media_file_id: Optional[UUID],
    about: Optional[str],
    admin_notes: Optional[str]
) -> UserData:

    user_obj = get_user_object(user_id)
    enshure_db_object_exists(User, user_obj)
    user_data_obj = user_obj.user_data

    # check user_data email unique
    user_data_duplicate = UserData.query.filter_by(email=email).first()
    if user_data_duplicate and user_data_duplicate.id != user_data_obj.id:
        raise ApiValidateError(
            code="not_unique",
            msg_template='email is not unique',
            location="email",
        )

    user_data_obj.email = email
    user_data_obj.nick_name = nick_name
    user_data_obj.first_name = first_name
    user_data_obj.last_name = last_name
    user_data_obj.middle_name = middle_name
    user_data_obj.avatar_media_file_id = avatar_media_file_id
    user_data_obj.about = about
    user_data_obj.admin_notes = admin_notes
    user_data_obj.mark_as_modified(user_modified_id)

    return user_data_obj
