from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
import src.conf.permissions as permissions
from src.pii__api__general.routes import api_bp
from src.conf.pii__api__general import api_general
from src.pii__db__general.helpers.organization_team_user.add_new_organization_team_user import \
    add_user_to_org_team
from src.pii__db__general.helpers.organization_team_user.delete_organization_team_user import \
    delete_organization_team_user
from src.pii__db__general.helpers.user.get_user import \
    get_organization_team_users_count, get_organization_team_users


@api_bp.route('/organizations/<uuid:organization_id>/teams/<uuid:organization_team_id>/users', methods=['GET'])
@api_general.rest_api(many=True, access=permissions.PERMISSION__PII_GET_ORG_TEAM_USERS_LIST)
def pii_get_org_team_users_list(
        api_resource: ApiResource,
        organization_id: UUID,
        organization_team_id: UUID
) -> TJsonResponse:
    organization_team_users = get_organization_team_users(
        organization_id=organization_id,
        organization_team_id=organization_team_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_organization_team_users_count(
        organization_id=organization_id,
        organization_team_id=organization_team_id,
    )
    organization_team_users = [org_team_user.to_dict() for org_team_user in organization_team_users]
    return api_resource.response_list_ok(organization_team_users, total_count)


@api_bp.route('/organizations/current/teams/<uuid:organization_team_id>/users', methods=['GET'])
@api_general.rest_api(many=True, access=api_general.ACCESS_PRIVATE)
def pii_get_current_org_team_users_list(
        api_resource: ApiResource,
        organization_team_id: UUID
) -> TJsonResponse:
    current_organization_team_users = get_organization_team_users(
        organization_team_id=organization_team_id,
        organization_id=api_resource.auth_token.organization_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_organization_team_users_count(
        organization_id=api_resource.auth_token.organization_id,
        organization_team_id=organization_team_id
    )
    current_organization_team_users = [user.to_dict() for user in current_organization_team_users]
    return api_resource.response_list_ok(current_organization_team_users, total_count)


@api_bp.route('/organizations/<uuid:organization_id>/teams/<uuid:organization_team_id>/users/<uuid:user_id>', methods=["PUT"])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_ADD_USER_TO_ORG_TEAM)
def pii_add_user_to_org_team(
        api_resource: ApiResource,
        organization_id: UUID,
        organization_team_id: UUID,
        user_id: UUID,
) -> TJsonResponse:
    with transaction_commit():
        new_organization_team_user = add_user_to_org_team(
            user_id=user_id,
            organization_id=organization_id,
            organization_team_id=organization_team_id,
            user_created_id=api_resource.auth_token.user_id,
        )
    return api_resource.response_obj_created_ok(new_organization_team_user.to_dict())


@api_bp.route('/organizations/current/teams/<uuid:organization_team_id>/users/<uuid:user_id>', methods=["PUT"])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_ADD_USER_TO_CURRENT_ORG_TEAM)
def pii_add_user_to_current_org_team(
        api_resource: ApiResource,
        organization_team_id: UUID,
        user_id: UUID,
) -> TJsonResponse:
    with transaction_commit():
        new_current_organization_team_user = add_user_to_org_team(
            user_id=user_id,
            user_created_id=api_resource.auth_token.user_id,
            organization_team_id=organization_team_id,
            organization_id=api_resource.auth_token.organization_id
        )
    return api_resource.response_obj_created_ok(new_current_organization_team_user.to_dict())


@api_bp.route('/organizations/<uuid:organization_id>/teams/<uuid:organization_team_id>/users/'
              '<uuid:organization_team_user_id>', methods=['DELETE'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_DEL_USER_FROM_ORG_TEAM)
def pii_del_user_from_org_team(
        api_resource: ApiResource,
        organization_id: UUID,
        organization_team_id: UUID,
        organization_team_user_id: UUID,
) -> TJsonResponse:
    with transaction_commit():
        delete_organization_team_user(
            organization_team_user_id=organization_team_user_id,
            user_deleted_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_deleted_ok()


@api_bp.route('/organizations/current/teams/<uuid:organization_team_id>/users/'
              '<uuid:organization_team_user_id>', methods=['DELETE'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_DEL_USER_FROM_CURRENT_ORG_TEAM)
def pii_del_user_from_current_org_team(
        api_resource: ApiResource,
        organization_team_id: UUID,
        organization_team_user_id: UUID,
) -> TJsonResponse:
    with transaction_commit():
        delete_organization_team_user(
            organization_team_user_id=organization_team_user_id,
            user_deleted_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_deleted_ok()
