from typing import Any, Dict

from api_utils.modules.api_sdk_jwt import ApiSdkJwt

from src.utils.invalid_credentials_error import invalid_credentials_error
from src.conf.pii__api__auth import api_auth
from src.pii__db__general.helpers.user.get_user import get_user_permissions_by_organization
from src.pii__db__general.helpers.organization.get_organization import get_first_user_organization
from src.utils.check_password import check_password
from src.pii__db__general.models.user_credentials import UserCredentials


def create_new_tokens(login: str, password: str) -> Dict[str, Any]:
    user_credentials = UserCredentials.query.filter_by(login=login).first()
    if user_credentials is None:
        invalid_credentials_error()
    if not check_password(password, user_credentials.password):
        invalid_credentials_error()
    user_organization = get_first_user_organization(user_credentials.user_id)
    user_permissions = get_user_permissions_by_organization(
        user_id=user_credentials.user_id,
        organization_id=user_organization.id
    )
    id, at, rt = api_auth.create_jwt_access_refresh_token(
        user_id=user_credentials.user_id,
        organization_id=user_organization.id,
        permissions=user_permissions,
        additional_data=None,
    )
    return {
        'id': str(id),
        'user_id': user_credentials.user_id,
        'access_token': at,
        'refresh_token': rt,
    }


def update_tokens(payload: ApiSdkJwt) -> Dict[str, Any]:
    user_organization = get_first_user_organization(payload.user_id)
    user_permissions = get_user_permissions_by_organization(
        user_id=payload.user_id,
        organization_id=user_organization.id
    )
    id, at, rt = api_auth.create_jwt_access_refresh_token(
        user_id=payload.user_id,
        organization_id=user_organization.id,
        permissions=user_permissions,
        additional_data=None,
    )
    return {
        'id': str(id),
        'access_token': at,
        'refresh_token': rt,
    }
