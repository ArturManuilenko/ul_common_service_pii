import os

from api_utils.modules.api_sdk_config import ApiSdkConfig
from api_utils.modules.api_utils_sdk import ApiSdk

API__VERSION = 'v1'

jwt_public_key_path = os.environ['JWT_PUBLIC_KEY_PATH']
with open(jwt_public_key_path, 'r+') as f:
    jwt_public_key = f.read()

jwt_private_key_path = os.environ['JWT_PRIVATE_KEY_PATH']
with open(jwt_private_key_path, 'r+') as f:
    jwt_private_key = f.read()

api_auth = ApiSdk(ApiSdkConfig(
    environment=os.environ['APPLICATION_ENV'],
    jwt_public_key=jwt_public_key,
    jwt_private_key=jwt_private_key,
    check_access=False,
    debug=False,
))
