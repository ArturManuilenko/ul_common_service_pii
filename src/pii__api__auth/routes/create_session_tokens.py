
from db_utils.modules.transaction_commit import transaction_commit
from src.pii__db__general.models.user_auth_log import UserAuthLogType
from src.pii__db__general.helpers.auth_log.add_user_auth_log import add_user_auth_log
from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.errors.api_validate_error import ApiValidateError
from api_utils.utils.constants import TJsonResponse
from pydantic import BaseModel, validator

from src.conf.api import Config
from src.utils.decrypt_credentials import decrypt_credentials
from src.pii__db__auth.helpers.refresh_token import store_refresh_token
from src.conf.pii__api__auth import api_auth
from src.pii__api__auth.routes import api_bp
from src.pii__db__auth.helpers.xor_actions import get_xor_token
from src.pii__db__general.helpers.auth.create_new_session_jwt_tokens import create_new_tokens


class ApiCreateSessionTokens(BaseModel):
    login: str
    password: str

    @validator('password')
    def check_password_length(cls, v: str) -> str:  # noqa
        if not len(v) >= 6:
            raise ApiValidateError(
                code='login/password_error',
                location=['password'],
                msg_template='password length must be more than 6 symbols',
            )
        return v


@api_bp.route('/session-tokens/<uuid:xor_id>/sessions', methods=['POST'])
@api_auth.rest_api(many=False, access=api_auth.ACCESS_PUBLIC)
def pii_jwt_mk(api_resource: ApiResource, xor_id: UUID, body: ApiCreateSessionTokens) -> TJsonResponse:
    xor_token = get_xor_token(xor_id)
    unxored_password = decrypt_credentials(body.password, xor_token)
    unxored_login = decrypt_credentials(body.login, xor_token)
    tokens = create_new_tokens(unxored_login, unxored_password)
    tokens_id = tokens.pop('id')
    user_id = tokens.pop('user_id')
    with transaction_commit():
        add_user_auth_log(
            type=UserAuthLogType.login,
            user_id=user_id,
            user_agent=api_resource.auth_log.user_agent,
            ipv4=api_resource.auth_log.ipv4,
            user_created_id=user_id
        )
    store_refresh_token(tokens_id, Config.JWT_TOKEN_SET_TIME)
    return api_resource.response_obj_ok(tokens)
