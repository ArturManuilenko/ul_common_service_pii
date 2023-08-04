from uuid import UUID

from db_utils.utils.query_soft_delete import query_soft_delete
from src.pii__db__general.models.user import User


def delete_user(user_id: UUID, user_deleted_id: UUID) -> None:
    query_soft_delete(User, user_id, user_deleted_id)
