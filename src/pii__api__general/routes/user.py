
from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
import src.conf.permissions as permissions
from src.conf.pii__api__general import api_general
from src.pii__api__general.routes import api_bp
from src.pii__db__general.helpers.user.delete_user import delete_user
from src.pii__db__general.helpers.user.get_user import get_organization_user, get_user_list, \
    get_user_object, get_user_total_count, get_organization_users, get_organization_users_count
from src.pii__db__general.helpers.user_data.update_user_data import update_current_user_data_obj, \
    update_user_data_obj
from src.pii__api__general.validators.user import ApiUser


@api_bp.route('/users', methods=['GET'])
@api_general.rest_api(many=True, access=permissions.PERMISSION__PII_GET_USERS_LIST)
def pii_get_users_list(api_resource: ApiResource) -> TJsonResponse:
    users = get_user_list(
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_user_total_count()
    users = [user.to_dict() for user in users]
    return api_resource.response_list_ok(users, total_count)


@api_bp.route('/organizations/<uuid:organization_id>/users', methods=['GET'])
@api_general.rest_api(many=True, access=permissions.PERMISSION__PII_GET_ORG_USERS_LIST)
def pii_get_org_users_list(api_resource: ApiResource, organization_id: UUID) -> TJsonResponse:
    organization_users_list = get_organization_users(
        organization_id=organization_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_organization_users_count(organization_id)
    organization_users_list = [org_users.to_dict() for org_users in organization_users_list]
    return api_resource.response_list_ok(organization_users_list, total_count)


@api_bp.route('/organizations/current/users', methods=['GET'])
@api_general.rest_api(many=True, access=api_general.ACCESS_PRIVATE)
def pii_get_current_org_users_list(api_resource: ApiResource) -> TJsonResponse:
    organization_users_list = get_organization_users(
        organization_id=api_resource.auth_token.organization_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_organization_users_count(api_resource.auth_token.organization_id)
    organization_users_list = [org_users.to_dict() for org_users in organization_users_list]
    return api_resource.response_list_ok(organization_users_list, total_count)


@api_bp.route('/organizations/<uuid:organization_id>/users/<uuid:user_id>', methods=['GET'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_GET_ORG_USER)
def pii_get_org_user(
    api_resource: ApiResource,
    organization_id: UUID,
    user_id: UUID
) -> TJsonResponse:
    organization_user = get_organization_user(
        organization_id=organization_id,
        user_id=user_id
    )
    return api_resource.response_obj_ok(organization_user)


@api_bp.route('/organizations/current/users/<uuid:user_id>', methods=['GET'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PRIVATE)
def pii_get_current_org_user(
    api_resource: ApiResource,
    user_id: UUID
) -> TJsonResponse:
    organization_user = get_organization_user(
        organization_id=api_resource.auth_token.organization_id,
        user_id=user_id
    )
    return api_resource.response_obj_ok(organization_user)


@api_bp.route('/users/<uuid:user_id>', methods=['GET'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_GET_USER)
def pii_get_user(api_resource: ApiResource, user_id: UUID) -> TJsonResponse:
    user = get_user_object(user_id)
    return api_resource.response_obj_ok(user.to_dict())


@api_bp.route('/users/current', methods=['GET'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PRIVATE)
def pii_get_current_user(api_resource: ApiResource) -> TJsonResponse:
    user = get_user_object(api_resource.auth_token.user_id)
    return api_resource.response_obj_ok(user.to_dict())


@api_bp.route('/users-data/<uuid:user_data_id>', methods=['PUT'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_MOD_USER_DATA)
def pii_mod_user_data(api_resource: ApiResource, body: ApiUser, user_data_id: UUID) -> TJsonResponse:
    with transaction_commit():
        new_user = update_user_data_obj(
            user_data_id=user_data_id,
            user_modified_id=api_resource.auth_token.user_id,
            email=body.email,
            nick_name=body.nick_name,
            first_name=body.first_name,
            middle_name=body.middle_name,
            last_name=body.last_name,
            avatar_media_file_id=body.avatar_media_file_id,
            about=body.about,
            admin_notes=body.admin_notes,
        )
    return api_resource.response_obj_ok(new_user.to_dict())


@api_bp.route('/users-data/current', methods=['PUT'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PRIVATE)
def pii_mod_current_user_data(api_resource: ApiResource, body: ApiUser) -> TJsonResponse:
    with transaction_commit():
        new_current_user = update_current_user_data_obj(
            user_id=api_resource.auth_token.user_id,
            user_modified_id=api_resource.auth_token.user_id,
            email=body.email,
            nick_name=body.nick_name,
            first_name=body.first_name,
            middle_name=body.middle_name,
            last_name=body.last_name,
            avatar_media_file_id=body.avatar_media_file_id,
            about=body.about,
            admin_notes=body.admin_notes,
        )
    return api_resource.response_obj_ok(new_current_user.to_dict())


@api_bp.route('/users/<uuid:user_id>', methods=['DELETE'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_DEL_USER)
def pii_del_user(api_resource: ApiResource, user_id: UUID) -> TJsonResponse:
    with transaction_commit():
        delete_user(
            user_id=user_id,
            user_deleted_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_deleted_ok()
