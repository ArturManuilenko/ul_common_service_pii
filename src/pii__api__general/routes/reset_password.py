from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.errors.api_validate_error import ApiValidateError
from api_utils.errors.api_simple_validate_error import ApiSimpleValidateError
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
from src.conf.api import Config
from src.conf.pii__db__general import PII__DB__GENERAL__GUEST_USER_ID
from src.conf.pii__api__general import api_general
from src.pii__api__general.routes import api_bp
from src.pii__api__general.validators.user_credentials_request import ApiUserResetPassword, ApiUserResetPasswordRequest
from src.pii__db__general.models.user_credentials_request import UserCredentialsRequestType
from src.pii__db__general.helpers.user_credentials_request.get_user_credentials_request import get_user_credentials_request_object
from src.pii__db__general.helpers.user_credentials_request.confirm_credentials_request import confirm_credentials_request
from src.pii__db__general.helpers.user_credentials.get_user_credentials import get_user_credentials_object_by_login, get_user_credentials_object_by_user
from src.pii__db__general.helpers.user_credentials_request.add_new_user_credentials_request import add_new_reset_password_request
from src.pii__db__general.helpers.user_credentials.delete_user_credentials import delete_user_credentials
from src.pii__db__general.helpers.user_credentials.add_new_user_credentials import add_new_user_credentials
from src.pii__db__auth.helpers.xor_actions import get_xor_token
from src.pii__db__auth.helpers.generate_credentials_request_token import generate_credentials_request_token
from src.pii__db__auth.helpers.credentials_request_token import get_credentials_request_id, store_credentials_request_token
from src.utils.decrypt_credentials import decrypt_credentials


@api_bp.route('/credentials-reset', methods=['POST'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PUBLIC)
def pii_mk_credentials_request_reset(api_resource: ApiResource, body: ApiUserResetPasswordRequest) -> TJsonResponse:
    user_credentials = get_user_credentials_object_by_login(body.login)
    with transaction_commit():
        new_password_reset_request = add_new_reset_password_request(
            user_id=user_credentials.user_id,
            user_created_id=PII__DB__GENERAL__GUEST_USER_ID
        )
    new_password_reset_token = generate_credentials_request_token()
    store_credentials_request_token(
        credentials_request_id=new_password_reset_request.id,
        credentials_request_token=new_password_reset_token,
        ttl=Config.CREDENTIALS_REQUEST_TOKEN_SET_TIME
    )
    return api_resource.response_obj_ok(new_password_reset_request.to_dict())


@api_bp.route('/session-tokens/<uuid:xor_token_id>/credentials-reset/<uuid:credentials_reset_request_id>/credentials', methods=['POST'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PUBLIC)
def pii_mk_credentials_reset(
    api_resource: ApiResource,
    body: ApiUserResetPassword,
    xor_token_id: UUID,
    credentials_reset_request_id: UUID,
) -> TJsonResponse:
    xor_token = get_xor_token(xor_token_id)
    credentials_reset_request = get_user_credentials_request_object(
        type=UserCredentialsRequestType.reset_password,
        user_credentials_request_id=credentials_reset_request_id
    )
    if credentials_reset_request.id != get_credentials_request_id(body.credentials_request_token):
        raise ApiValidateError(
            code='credentials_request_token_error',
            location='credentials_request_token',
            msg_template="credentials request token is invalid"
        )
    if credentials_reset_request.date_confirmed:
        raise ApiSimpleValidateError('credentials reset request already confirmed')
    user_new_password = decrypt_credentials(body.new_password, xor_token)
    old_user_credentials = get_user_credentials_object_by_user(credentials_reset_request.user_id)
    with transaction_commit():
        add_new_user_credentials(
            login=old_user_credentials.login,
            password=user_new_password,
            user_credentials_request_id=credentials_reset_request.id,
            user_id=old_user_credentials.user_id,
            user_created_id=old_user_credentials.user_id,
            date_expiration=None,
        )
        confirm_credentials_request(credentials_reset_request.id, credentials_reset_request.user_id)
        delete_user_credentials(old_user_credentials.id, credentials_reset_request.user_id)
    return api_resource.response_obj_ok(credentials_reset_request.to_dict())
