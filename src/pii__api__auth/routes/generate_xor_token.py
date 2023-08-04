from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse

from src.conf.pii__api__auth import api_auth
from src.pii__api__auth.routes import api_bp
from src.pii__db__auth.helpers.xor_actions import generate_xor, store_xor_token


@api_bp.route('/session-tokens/new', methods=['GET'])
@api_auth.rest_api(many=False, access=api_auth.ACCESS_PUBLIC)
def pii_mk_xor_token(api_resource: ApiResource) -> TJsonResponse:
    xor_token = generate_xor()
    db_id = store_xor_token(xor_token)
    response = {
        'id': db_id,
        'xor_token': xor_token
    }
    return api_resource.response_obj_ok(response)
