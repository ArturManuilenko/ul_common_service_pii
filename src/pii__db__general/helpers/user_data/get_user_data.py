from typing import List
from uuid import UUID
from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.pii__db__general.models.user_data import UserData


def get_user_data_object(user_data_id: UUID) -> UserData:
    user_data = UserData.query.filter_by(id=user_data_id).first()
    return enshure_db_object_exists(UserData, user_data)


def get_user_data_list(limit: int, offset: int) -> List[UserData]:
    user_data_list = UserData.query.offset(offset).limit(limit).all()
    return user_data_list


def get_user_data_total_count() -> int:
    return UserData.query.count()
