from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
from db_utils.utils.get_model_template import get_models_template

import src.conf.permissions as permissions
from src.conf.permissions import permissions as permissions_registry
from src.pii__api__general.routes import api_bp
from src.conf.pii__api__general import api_general
from src.pii__db__general.helpers.organization_team.delete_organization_team import delete_organization_team
from src.pii__db__general.helpers.organization_team.get_organization_team import \
    get_organization_teams, get_organization_teams_count, get_organization_team_object, get_user_organization_teams, get_user_organization_teams_count
from src.pii__db__general.helpers.organization_team.update_organization_team import \
    update_organization_team_obj
from src.pii__db__general.models.organization_team import OrganizationTeam
from src.pii__api__general.validators.organization_team import ApiOrganizationTeam
from src.pii__db__general.helpers.organization_team.add_new_organization_team import \
    add_new_organization_team
from src.pii__db__general.helpers.user.get_user import get_organization_team_users_count


@api_bp.route('/organizations/<uuid:organization_id>/teams', methods=['GET'])
@api_general.rest_api(many=True, access=permissions.PERMISSION__PII_GET_ORG_TEAMS_LIST)
def pii_get_org_teams_list(api_resource: ApiResource, organization_id: UUID) -> TJsonResponse:
    organization_teams_objects = get_organization_teams(
        organization_id=organization_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_organization_teams_count(organization_id)
    organization_teams = []
    for organization_team in organization_teams_objects:
        organization_team = organization_team.to_dict()
        organization_team['users_count'] = get_organization_team_users_count(
            organization_id=organization_id,
            organization_team_id=organization_team['id']
        )
        organization_teams.append(organization_team)
    return api_resource.response_list_ok(organization_teams, total_count)


@api_bp.route('/organizations/current/teams', methods=['GET'])
@api_general.rest_api(many=True, access=api_general.ACCESS_PRIVATE)
def pii_get_current_org_teams_list(api_resource: ApiResource) -> TJsonResponse:
    current_organization_teams_objects = get_organization_teams(
        organization_id=api_resource.auth_token.organization_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_organization_teams_count(api_resource.auth_token.organization_id)
    current_organization_teams = []
    for organization_team in current_organization_teams_objects:
        organization_team = organization_team.to_dict()
        organization_team['users_count'] = get_organization_team_users_count(
            organization_id=api_resource.auth_token.organization_id,
            organization_team_id=organization_team['id']
        )
        current_organization_teams.append(organization_team)
    return api_resource.response_list_ok(current_organization_teams, total_count)


@api_bp.route('/users/current/teams', methods=['GET'])
@api_general.rest_api(many=True, access=api_general.ACCESS_PRIVATE)
def pii_get_current_user_teams_list(api_resource: ApiResource) -> TJsonResponse:
    user_org_teams_objects = get_user_organization_teams(
        user_id=api_resource.auth_token.user_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_user_organization_teams_count(api_resource.auth_token.user_id)
    user_org_teams = [team.to_dict() for team in user_org_teams_objects]
    return api_resource.response_list_ok(user_org_teams, total_count)


@api_bp.route('/users/<uuid:user_id>/teams', methods=['GET'])
@api_general.rest_api(many=True, access=permissions.PERMISSION__PII_GET_USER_TEAMS_LIST)
def pii_get_user_teams_list(api_resource: ApiResource, user_id: UUID) -> TJsonResponse:
    user_org_teams_objects = get_user_organization_teams(
        user_id=user_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_user_organization_teams_count(api_resource.auth_token.user_id)
    user_org_teams = [team.to_dict() for team in user_org_teams_objects]
    return api_resource.response_list_ok(user_org_teams, total_count)


@api_bp.route('/organizations/<uuid:organization_id>/teams/<uuid:organization_team_id>', methods=['GET'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_GET_ORG_TEAM)
def pii_get_org_team(
    api_resource: ApiResource,
    organization_id: UUID,
    organization_team_id: UUID
) -> TJsonResponse:
    organization_team = get_organization_team_object(
        organization_id=organization_id,
        organization_team_id=organization_team_id
    )
    organization_team = organization_team.to_dict()
    organization_team['users_count'] = get_organization_team_users_count(
        organization_id=organization_id,
        organization_team_id=organization_team['id']
    )
    return api_resource.response_obj_ok(organization_team)


@api_bp.route('/organizations/current/teams/<uuid:organization_team_id>', methods=['GET'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PRIVATE)
def pii_get_current_org_team(
    api_resource: ApiResource,
    organization_team_id: UUID
) -> TJsonResponse:
    organization_team = get_organization_team_object(
        organization_id=api_resource.auth_token.organization_id,
        organization_team_id=organization_team_id
    )
    organization_team = organization_team.to_dict()
    organization_team['users_count'] = get_organization_team_users_count(
        organization_id=api_resource.auth_token.organization_id,
        organization_team_id=organization_team['id']
    )
    return api_resource.response_obj_ok(organization_team)


@api_bp.route('/teams/new', methods=['GET'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_GET_ORG_TEAM_TPL)
def pii_get_org_team_tpl(api_resource: ApiResource) -> TJsonResponse:
    team_fields = get_models_template([OrganizationTeam])
    # set avaliable permissions to create org team with avalibale permissions for whole organization
    team_fields['permissions'] = permissions_registry.get_ids_from_iterable(
        permissions.DEFAULT_ORGANIZATION_AVAILABLE_PERMISSION_LIST
    )
    return api_resource.response_obj_ok(team_fields)


@api_bp.route('/organizations/<uuid:organization_id>/teams', methods=["POST"])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_MK_ORG_TEAM)
def pii_mk_org_team(
        api_resource: ApiResource,
        organization_id: UUID,
        body: ApiOrganizationTeam
) -> TJsonResponse:
    with transaction_commit():
        new_organization_team = add_new_organization_team(
            organization_id=organization_id,
            name=body.name,
            permissions=body.permissions,
            is_organization_admin=body.is_organization_admin,
            user_created_id=api_resource.auth_token.user_id,
        )
    new_organization_team = new_organization_team.to_dict()
    new_organization_team['users_count'] = get_organization_team_users_count(
        organization_id=organization_id,
        organization_team_id=new_organization_team['id']
    )
    return api_resource.response_obj_created_ok(new_organization_team)


@api_bp.route('/organizations/current/teams', methods=["POST"])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_MK_CURRENT_ORG_TEAM)
def pii_mk_current_org_team(
        api_resource: ApiResource,
        body: ApiOrganizationTeam
) -> TJsonResponse:
    with transaction_commit():
        new_organization_team = add_new_organization_team(
            organization_id=api_resource.auth_token.organization_id,
            name=body.name,
            permissions=body.permissions,
            is_organization_admin=body.is_organization_admin,
            user_created_id=api_resource.auth_token.user_id,
        )
    new_organization_team = new_organization_team.to_dict()
    new_organization_team['users_count'] = get_organization_team_users_count(
        organization_id=api_resource.auth_token.organization_id,
        organization_team_id=new_organization_team['id']
    )
    return api_resource.response_obj_created_ok(new_organization_team)


@api_bp.route('/organizations/<uuid:organization_id>/teams/<uuid:organization_team_id>', methods=['PUT'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_MOD_ORG_TEAM)
def pii_mod_org_team(
        api_resource: ApiResource,
        body: ApiOrganizationTeam,
        organization_id: UUID,
        organization_team_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        new_organization_team = update_organization_team_obj(
            name=body.name,
            permissions=body.permissions,
            is_organization_admin=body.is_organization_admin,
            user_modified_id=api_resource.auth_token.user_id,
            organization_team_id=organization_team_id,
            organization_id=organization_id
        )
        new_organization_team = new_organization_team.to_dict()
        new_organization_team['users_count'] = get_organization_team_users_count(
            organization_id=organization_id,
            organization_team_id=new_organization_team['id']
        )
    return api_resource.response_obj_ok(new_organization_team)


@api_bp.route('/organizations/current/teams/<uuid:organization_team_id>', methods=['PUT'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_MOD_CURRENT_ORG_TEAM)
def pii_mod_current_org_team(
        api_resource: ApiResource,
        body: ApiOrganizationTeam,
        organization_team_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        new_current_organization_team = update_organization_team_obj(
            name=body.name,
            permissions=body.permissions,
            is_organization_admin=body.is_organization_admin,
            user_modified_id=api_resource.auth_token.user_id,
            organization_team_id=organization_team_id,
            organization_id=api_resource.auth_token.organization_id
        )
    new_current_organization_team = new_current_organization_team.to_dict()
    new_current_organization_team['users_count'] = get_organization_team_users_count(
        organization_id=api_resource.auth_token.organization_id,
        organization_team_id=new_current_organization_team['id']
    )
    return api_resource.response_obj_ok(new_current_organization_team)


@api_bp.route('/organizations/<uuid:organization_id>/teams/<uuid:organization_team_id>', methods=['DELETE'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_DEL_ORG_TEAM)
def pii_del_org_team(
        api_resource: ApiResource,
        organization_id: UUID,
        organization_team_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        delete_organization_team(
            organization_team_id=organization_team_id,
            user_deleted_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_deleted_ok()


@api_bp.route('/organizations/current/teams/<uuid:organization_team_id>', methods=['DELETE'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_DEL_CURRENT_ORG_TEAM)
def pii_del_current_org_team(
        api_resource: ApiResource,
        organization_team_id: UUID
) -> TJsonResponse:
    with transaction_commit():
        delete_organization_team(
            organization_team_id=organization_team_id,
            user_deleted_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_deleted_ok()
