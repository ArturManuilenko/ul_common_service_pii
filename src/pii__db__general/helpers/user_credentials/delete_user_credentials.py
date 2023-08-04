from uuid import UUID

from db_utils.utils.query_soft_delete import query_soft_delete
from src.pii__db__general.models.user_credentials import UserCredentials


def delete_user_credentials(user_credentials_id: UUID, user_deleted_id: UUID) -> None:
    query_soft_delete(UserCredentials, user_credentials_id, user_deleted_id)
