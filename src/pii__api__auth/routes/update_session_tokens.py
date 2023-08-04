from db_utils.modules.transaction_commit import transaction_commit
from api_utils.api_resource.api_resource import ApiResource
from api_utils.errors.api_no_result_found import ApiNoResultFoundError
from api_utils.utils.constants import TJsonResponse

from src.conf.api import Config
from src.conf.pii__api__auth import api_auth
from src.pii__api__auth.routes import api_bp
from src.pii__db__auth.helpers.refresh_token import has_refresh_token, delete_refresh_token, store_refresh_token
from src.pii__db__general.helpers.auth.create_new_session_jwt_tokens import update_tokens
from src.pii__db__general.models.user_auth_log import UserAuthLogType
from src.pii__db__general.helpers.auth_log.add_user_auth_log import add_user_auth_log


@api_bp.route('/sessions/current', methods=['PUT'])
@api_auth.rest_api(many=False, access=api_auth.ACCESS_PRIVATE_RT)
def pii_jwt_mod(api_resource: ApiResource) -> TJsonResponse:
    if not has_refresh_token(str(api_resource.auth_token.id)):
        raise ApiNoResultFoundError("jwt token doesn't exist")
    delete_refresh_token(str(api_resource.auth_token.id))
    tokens = update_tokens(api_resource.auth_token)
    with transaction_commit():
        add_user_auth_log(
            type=UserAuthLogType.refresh_auth,
            user_id=api_resource.auth_token.user_id,
            user_agent=api_resource.auth_log.user_agent,
            ipv4=api_resource.auth_log.ipv4,
            user_created_id=api_resource.auth_token.user_id
        )
    store_refresh_token(tokens.pop('id'), Config.JWT_TOKEN_SET_TIME)
    return api_resource.response_obj_ok(tokens)
