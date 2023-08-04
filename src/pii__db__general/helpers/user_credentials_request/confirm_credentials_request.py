from uuid import UUID

from src.pii__db__general.helpers.user.get_user import get_user_object
from db_utils.utils.enshure_db_object_exists import enshure_db_object_exists
from src.pii__db__general.models.user_credentials_request import UserCredentialsRequest


def confirm_credentials_request(
    user_credentials_request_id: UUID,
    user_modified_id: UUID,
) -> None:
    '''Util for confirm any credentials request'''
    user_credentials_request = UserCredentialsRequest.query.filter_by(id=user_credentials_request_id).first()
    enshure_db_object_exists(UserCredentialsRequest, user_credentials_request)
    user_credentials_request.mark_as_modified(user_modified_id)


def confirm_invite(
    user_credentials_request_id: UUID,
    user_id: UUID,
    user_modified_id: UUID,
) -> None:
    '''Util for confirm invite request with write new user id to credentails request'''
    get_user_object(user_id)
    user_credentials_request = UserCredentialsRequest.query.filter_by(id=user_credentials_request_id).first()
    enshure_db_object_exists(UserCredentialsRequest, user_credentials_request)
    user_credentials_request.mark_as_modified(user_modified_id)
