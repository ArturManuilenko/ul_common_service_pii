

from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.errors.api_simple_validate_error import ApiSimpleValidateError
from api_utils.errors.api_validate_error import ApiValidateError
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
from src.conf.api import Config
from src.utils.check_password import check_password
from src.utils.decrypt_credentials import decrypt_credentials
from src.conf.pii__api__general import api_general
from src.pii__api__general.routes import api_bp
from src.pii__api__general.validators.user_credentials_request import ApiUserChangePassword
from src.pii__db__general.models.user_credentials_request import UserCredentialsRequestType
from src.pii__db__general.helpers.user_credentials_request.get_user_credentials_request import get_user_credentials_request_object
from src.pii__db__general.helpers.user_credentials_request.confirm_credentials_request import confirm_credentials_request
from src.pii__db__general.helpers.user_credentials.get_user_credentials import get_user_credentials_object_by_user
from src.pii__db__general.helpers.user_credentials_request.add_new_user_credentials_request import add_new_change_password_request
from src.pii__db__general.helpers.user_credentials.delete_user_credentials import delete_user_credentials
from src.pii__db__general.helpers.user_credentials.add_new_user_credentials import add_new_user_credentials
from src.pii__db__auth.helpers.xor_actions import get_xor_token
from src.pii__db__auth.helpers.credentials_request_token import get_credentials_request_id, store_credentials_request_token
from src.pii__db__auth.helpers.generate_credentials_request_token import generate_credentials_request_token


@api_bp.route('/users/current/credentials-change', methods=['POST'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PRIVATE)
def pii_mk_current_credentials_request_change(api_resource: ApiResource) -> TJsonResponse:
    with transaction_commit():
        new_password_change_request = add_new_change_password_request(
            user_id=api_resource.auth_token.user_id,
            user_created_id=api_resource.auth_token.user_id
        )
    new_password_change_token = generate_credentials_request_token()
    store_credentials_request_token(
        credentials_request_id=new_password_change_request.id,
        credentials_request_token=new_password_change_token,
        ttl=Config.CREDENTIALS_REQUEST_TOKEN_SET_TIME
    )
    return api_resource.response_obj_ok(new_password_change_request.to_dict())


@api_bp.route('/session-tokens/<uuid:xor_token_id>/credentials-change/<uuid:credentials_change_request_id>/credentials', methods=['POST'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PRIVATE)
def pii_mk_credentials_change(
    api_resource: ApiResource,
    body: ApiUserChangePassword,
    xor_token_id: UUID,
    credentials_change_request_id: UUID,
) -> TJsonResponse:
    xor_token = get_xor_token(xor_token_id)
    credentials_change_request = get_user_credentials_request_object(
        type=UserCredentialsRequestType.change_password,
        user_credentials_request_id=credentials_change_request_id
    )
    if credentials_change_request.id != get_credentials_request_id(body.credentials_request_token):
        raise ApiValidateError(
            code='credentials_request_token_error',
            location='body.credentials_request_token',
            msg_template="credentials request id is invalid"
        )
    if credentials_change_request.date_confirmed:
        raise ApiSimpleValidateError('credentials change request already confirmed')

    user_credentials = get_user_credentials_object_by_user(api_resource.auth_token.user_id)
    user_old_password = decrypt_credentials(body.old_password, xor_token)
    if not check_password(user_old_password.encode('utf8'), user_credentials.password):
        raise ApiValidateError(
            code='password_error',
            location=['password'],
            msg_template='old password is wrong',
        )
    user_new_password = decrypt_credentials(body.new_password, xor_token)
    with transaction_commit():
        add_new_user_credentials(
            login=user_credentials.login,
            password=user_new_password,
            user_credentials_request_id=credentials_change_request.id,
            user_id=api_resource.auth_token.user_id,
            user_created_id=credentials_change_request.user_id,
            date_expiration=None,
        )
        confirm_credentials_request(credentials_change_request.id, api_resource.auth_token.user_id)
        delete_user_credentials(user_credentials.id, credentials_change_request.user_id)
    return api_resource.response_obj_ok(credentials_change_request.to_dict())
