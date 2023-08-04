from uuid import UUID

from src.pii__db__general.models.user_data import UserData
from db_utils.utils.query_soft_delete import query_soft_delete


def delete_user_data(user_data_id: UUID, user_deleted_id: UUID) -> None:
    query_soft_delete(UserData, user_data_id, user_deleted_id)
