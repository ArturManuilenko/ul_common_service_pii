from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse

from src.conf.pii__api__auth import api_auth
from src.pii__api__auth.routes import api_bp
from src.pii__db__auth.helpers.refresh_token import has_refresh_token, delete_refresh_token


@api_bp.route('/sessions/current', methods=['DELETE'])
@api_auth.rest_api(many=False, access=api_auth.ACCESS_PRIVATE_RT)
def pii_jwt_del(api_resource: ApiResource) -> TJsonResponse:
    token_id = api_resource.auth_token.id
    if not has_refresh_token(str(token_id)):
        return api_resource.response_obj_deleted_ok()
    delete_refresh_token(str(token_id))
    return api_resource.response_obj_deleted_ok()
