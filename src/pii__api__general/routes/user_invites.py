from uuid import UUID

from api_utils.errors.api_simple_validate_error import ApiSimpleValidateError
from api_utils.api_resource.api_resource import ApiResource
from api_utils.errors.api_validate_error import ApiValidateError
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
from db_utils.utils.get_model_template import get_models_template
import src.conf.permissions as permissions
from src.conf.api import Config
from src.conf.pii__api__general import api_general
from src.pii__api__general.routes import api_bp
from src.pii__api__general.validators.user import ApiUser
from src.pii__db__general.models.user_data import UserData
from src.pii__db__general.models.user_credentials_request import UserCredentialsRequestType
from src.pii__api__general.validators.user_credentials_request import ApiUserInvite
from src.pii__db__general.helpers.user_data.add_new_user_data import add_new_user_data
from src.pii__db__general.helpers.user_data.get_user_data import get_user_data_object
from src.pii__db__general.helpers.user_credentials_request.add_new_user_credentials_request import add_new_user_invite_request
from src.pii__db__general.helpers.user_credentials_request.get_user_credentials_request import \
    get_credentials_request_by_org_total_count, get_user_credentials_request_list_by_org, get_user_credentials_request_object
from src.pii__db__auth.helpers.credentials_request_token import get_credentials_request_id, store_credentials_request_token
from src.pii__db__general.helpers.user_credentials_request.confirm_credentials_request import confirm_invite
from src.pii__db__general.helpers.user_credentials_request.delete_user_credentials_request import delete_user_credentials_request
from src.pii__db__general.helpers.user_credentials.add_new_user_credentials import add_new_user_credentials
from src.pii__db__general.helpers.user.add_new_user import add_new_user_with_existing_data
from src.pii__db__auth.helpers.generate_credentials_request_token import generate_credentials_request_token
from src.pii__db__auth.helpers.xor_actions import get_xor_token
from src.utils.decrypt_credentials import decrypt_credentials


@api_bp.route('/organizations/<uuid:organization_id>/user-invites', methods=['GET'])
@api_general.rest_api(many=True, access=permissions.PERMISSION__PII_GET_ORG_USER_INVITES_LIST)
def pii_get_org_user_invites_list(api_resource: ApiResource, organization_id: UUID) -> TJsonResponse:
    org_user_invites_list = get_user_credentials_request_list_by_org(
        type=UserCredentialsRequestType.invite,
        organization_id=organization_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset
    )
    user_invites_total_count_in_org = get_credentials_request_by_org_total_count(organization_id)
    org_user_invites_list = [org_user_invite.to_dict() for org_user_invite in org_user_invites_list]
    return api_resource.response_list_ok(org_user_invites_list, user_invites_total_count_in_org)


@api_bp.route('/organizations/current/user-invites', methods=['GET'])
@api_general.rest_api(many=True, access=permissions.PERMISSION__PII_GET_CURRENT_ORG_USER_INVITES_LIST)
def pii_get_current_org_user_invites_list(api_resource: ApiResource) -> TJsonResponse:
    org_user_invites_list = get_user_credentials_request_list_by_org(
        type=UserCredentialsRequestType.invite,
        organization_id=api_resource.auth_token.organization_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset
    )
    user_invites_total_count_in_org = get_credentials_request_by_org_total_count(api_resource.auth_token.organization_id)
    org_user_invites_list = [org_user_invite.to_dict() for org_user_invite in org_user_invites_list]
    return api_resource.response_list_ok(org_user_invites_list, user_invites_total_count_in_org)


@api_bp.route('/user-invites/<uuid:user_invite_request_id>', methods=['GET'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_GET_USER_INVITE)
def pii_get_user_invite(api_resource: ApiResource, user_invite_request_id: UUID) -> TJsonResponse:
    user_invite_obj = get_user_credentials_request_object(
        type=UserCredentialsRequestType.invite,
        user_credentials_request_id=user_invite_request_id
    )
    return api_resource.response_obj_ok(user_invite_obj.to_dict())


@api_bp.route('/user-invites/<user_invite_request_token>', methods=['GET'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PUBLIC)
def pii_get_user_invite_by_token(api_resource: ApiResource, user_invite_request_token: str) -> TJsonResponse:
    user_invite_id = get_credentials_request_id(user_invite_request_token)
    user_invite_obj = get_user_credentials_request_object(
        type=UserCredentialsRequestType.invite,
        user_credentials_request_id=UUID(user_invite_id)
    )
    return api_resource.response_obj_ok(user_invite_obj.to_dict())


@api_bp.route('/user-invites/new', methods=['GET'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_GET_USER_INVITE_TPL)
def pii_get_user_invite_tpl(api_resource: ApiResource) -> TJsonResponse:
    user_invite_tpl = get_models_template(UserData)
    return api_resource.response_obj_ok(user_invite_tpl)


@api_bp.route('/organizations/<uuid:org_id>/teams/<uuid:org_team_id>/user-invites', methods=['POST'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_MK_USER_INVITE_TO_ORG_TEAM)
def pii_mk_user_invite_to_org_team(
    api_resource: ApiResource,
    body: ApiUser,
    org_id: UUID,
    org_team_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        new_user_data = add_new_user_data(
            email=body.email,
            nick_name=body.nick_name,
            first_name=body.first_name,
            middle_name=body.middle_name,
            last_name=body.last_name,
            avatar_media_file_id=body.avatar_media_file_id,
            about=body.about,
            admin_notes=body.admin_notes,
            user_created_id=api_resource.auth_token.user_id
        )
        new_user_invite_obj = add_new_user_invite_request(
            user_data_id=new_user_data.id,
            organization_id=org_id,
            organization_team_id=org_team_id,
            user_created_id=api_resource.auth_token.user_id
        )
    user_invite_token = generate_credentials_request_token()
    store_credentials_request_token(
        credentials_request_id=new_user_invite_obj.id,
        credentials_request_token=user_invite_token,
        ttl=Config.CREDENTIALS_REQUEST_TOKEN_SET_TIME
    )
    return api_resource.response_obj_ok(new_user_invite_obj.to_dict())


@api_bp.route('/organizations/current/teams/<uuid:org_team_id>/user-invites', methods=['POST'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_MK_USER_INVITE_TO_CURRENT_ORG_TEAM)
def pii_mk_user_invite_to_current_org_team(
    api_resource: ApiResource,
    body: ApiUser,
    org_team_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        new_user_data = add_new_user_data(
            email=body.email,
            nick_name=body.nick_name,
            first_name=body.first_name,
            middle_name=body.middle_name,
            last_name=body.last_name,
            avatar_media_file_id=body.avatar_media_file_id,
            about=body.about,
            admin_notes=body.admin_notes,
            user_created_id=api_resource.auth_token.user_id
        )
        new_user_invite_obj = add_new_user_invite_request(
            user_data_id=new_user_data.id,
            organization_id=api_resource.auth_token.organization_id,
            organization_team_id=org_team_id,
            user_created_id=api_resource.auth_token.user_id
        )
    user_invite_token = generate_credentials_request_token()
    store_credentials_request_token(
        credentials_request_id=new_user_invite_obj.id,
        credentials_request_token=user_invite_token,
        ttl=Config.CREDENTIALS_REQUEST_TOKEN_SET_TIME
    )
    return api_resource.response_obj_ok(new_user_invite_obj.to_dict())


@api_bp.route('/session-tokens/<uuid:xor_token_id>/user-invites/<uuid:user_invite_request_id>/credentials', methods=['POST'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PUBLIC)
def pii_jwt_mk(
    api_resource: ApiResource,
    xor_token_id: UUID,
    user_invite_request_id: UUID,
    body: ApiUserInvite
) -> TJsonResponse:
    xor_token = get_xor_token(xor_token_id)
    invite_request = get_user_credentials_request_object(
        type=UserCredentialsRequestType.invite,
        user_credentials_request_id=user_invite_request_id
    )
    if str(invite_request.id) != get_credentials_request_id(body.credentials_request_token):
        raise ApiValidateError(
            code='credentials_request_token_error',
            location='credentials_request_token',
            msg_template="credentials request token is invalid"
        )
    if invite_request.date_confirmed:
        raise ApiSimpleValidateError('invite already confirmed')
    user_data = get_user_data_object(invite_request.user_data_id)
    new_user_password = decrypt_credentials(body.password, xor_token)
    with transaction_commit():
        new_user = add_new_user_with_existing_data(user_data.id, invite_request.user_created_id)
        add_new_user_credentials(
            login=user_data.email,
            password=new_user_password,
            date_expiration=None,
            user_id=new_user.id,
            user_credentials_request_id=invite_request.id,
            user_created_id=new_user.id,
        )
        confirm_invite(invite_request.id, new_user.id, new_user.id)
    return api_resource.response_obj_ok(invite_request.to_dict())


@api_bp.route('/user-invites/<uuid:user_invite_request_id>', methods=['DELETE'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_DEL_USER_INVITE)
def pii_del_user_invite(api_resource: ApiResource, user_invite_request_id: UUID) -> TJsonResponse:
    with transaction_commit():
        delete_user_credentials_request(
            type=UserCredentialsRequestType.invite,
            user_credentials_request_id=user_invite_request_id,
            user_deleted_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_deleted_ok()
