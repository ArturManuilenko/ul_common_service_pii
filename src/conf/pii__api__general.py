import os

from api_utils.modules.api_sdk_config import ApiSdkConfig
from api_utils.modules.api_utils_sdk import ApiSdk

API__VERSION = 'v1'
AES256_ENC_KEY = os.environ['PII__API__AUTH__AES256_ENC_KEY']


jwt_public_key_path = os.environ['JWT_PUBLIC_KEY_PATH']
with open(jwt_public_key_path, 'r+') as f:
    jwt_public_key = f.read()

api_general = ApiSdk(ApiSdkConfig(
    environment=os.environ['APPLICATION_ENV'],
    jwt_public_key=jwt_public_key,
    check_access=True,
    debug=False,
))


# Service general db length constants list for api validators
# ------------------------------------------------

USER__MIN_ADMIN_NOTES_LENGTH = 0
USER__MAX_ADMIN_NOTES_LENGTH = 1000


USER_DATA__EMAIL__REGEX = r'^[\w\.\+\-]+\@[\w]+\.[a-z]+$'
USER_DATA__EMAIL__MIN_LENGTH = 0
USER_DATA__EMAIL__MAX_LENGTH = 255
USER_DATA__NICK_NAME__MIN_LENGTH = 0
USER_DATA__NICK_NAME__MAX_LENGTH = 255
USER_DATA__FIRST_NAME__MIN_LENGTH = 0
USER_DATA__FIRST_NAME__MAX_LENGTH = 255
USER_DATA__LAST_NAME__MIN_LENGTH = 0
USER_DATA__LAST_NAME__MAX_LENGTH = 255
USER_DATA__MIDDLE_NAME__MIN_LENGTH = 0
USER_DATA__MIDDLE_NAME__MAX_LENGTH = 255
USER_DATA__ABOUT__MIN_LENGTH = 0
USER_DATA__ABOUT__MAX_LENGTH = 1000


USER_CREDENTIALS__LOGIN__MIN_LENGTH = 0
USER_CREDENTIALS__LOGIN__MAX_LENGTH = 250
USER_CREDENTIALS__PASSWORD__MIN_LENGTH = 0
USER_CREDENTIALS__PASSWORD__MAX_LENGTH = 250


USER_CREDENTIALS_REQUEST__TOKEN_ALIASE__MIN_LENGTH = 0
USER_CREDENTIALS_REQUEST__TOKEN_ALIASE__MAX_LENGTH = 255


ORGANIZATION__ADMIN_NOTES__MIN_LENGTH = 0
ORGANIZATION__ADMIN_NOTES__MAX_LENGTH = 2000


ORGANIZATION_TEAM__NAME__MIN_LENGTH = 0
ORGANIZATION_TEAM__NAME__MAX_LENGTH = 255

ORGANIZATION_USER__NOTES__MIN_LENGTH = 0
ORGANIZATION_USER__NOTES__MAX_LENGTH = 1000


ORGANIZATION_DATA__NAME__MIN_LENGTH = 0
ORGANIZATION_DATA__NAME__MAX_LENGTH = 255

# ------------------------------------------------

ORGANIZATION_DEFAULT_ADMIN_TEAM_NAME = 'admin_users'
ORGANIZATION_DEFAULT_USERS_TEAM_NAME = 'other_users'
ORGANIZATION_DEFAULT_INACTIVE_TEAM_NAME = 'inactive_users'