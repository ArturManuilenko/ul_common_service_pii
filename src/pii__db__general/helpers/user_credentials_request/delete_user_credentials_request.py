from uuid import UUID

from src.pii__db__general.models.user_credentials_request import UserCredentialsRequestType
from src.pii__db__general.helpers.user_credentials_request.get_user_credentials_request import get_user_credentials_request_object


def delete_user_credentials_request(type: UserCredentialsRequestType, user_credentials_request_id: UUID, user_deleted_id: UUID) -> None:
    user_credentials_request_obj = get_user_credentials_request_object(
        type=type,
        user_credentials_request_id=user_credentials_request_id
    )
    user_credentials_request_obj.mark_as_deleted(user_deleted_id)
