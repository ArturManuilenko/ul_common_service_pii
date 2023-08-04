from uuid import UUID

import src.conf.permissions as permissions
from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from db_utils.modules.transaction_commit import transaction_commit
from src.pii__api__general.routes import api_bp
from src.conf.pii__api__general import api_general
from src.pii__db__general.helpers.get_model_fields import get_many_model_fields
from src.pii__db__general.helpers.organization.add_new_organization import add_new_organization
from src.pii__db__general.helpers.organization.delete_organization import delete_organization
from src.pii__db__general.helpers.organization.update_organization import update_organization
from src.pii__db__general.helpers.organization.create_organization_default_teams import \
    create_organization_default_teams
from src.pii__db__general.helpers.organization.get_organization import get_organization_object, \
    get_organization_list, get_organization_total_count, get_user_organizations, get_user_organizations_count
from src.pii__db__general.helpers.organization_team.get_organization_team import get_organization_teams_count
from src.pii__db__general.helpers.user.get_user import get_organization_users_count
from src.pii__db__general.models.organization import Organization
from src.pii__db__general.models.organization_data import OrganizationData
from src.pii__api__general.validators.organization import ApiOrganization


@api_bp.route('/organizations', methods=['GET'])
@api_general.rest_api(many=True, access=permissions.PERMISSION__PII_GET_ORG_LIST)
def pii_get_org_list(api_resource: ApiResource) -> TJsonResponse:
    organizations_objects = get_organization_list(
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_organization_total_count()
    organizations = []
    for organization in organizations_objects:
        organization = organization.to_dict()
        organization['teams_count'] = get_organization_teams_count(organization['id'])
        organization['users_count'] = get_organization_users_count(organization['id'])
        organizations.append(organization)
    return api_resource.response_list_ok(organizations, total_count)


@api_bp.route('/users/current/organizations', methods=['GET'])
@api_general.rest_api(many=True, access=api_general.ACCESS_PRIVATE)
def pii_get_current_user_organizations_list(api_resource: ApiResource) -> TJsonResponse:
    users_organizatons_objects = get_user_organizations(
        user_id=api_resource.auth_token.user_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_user_organizations_count(api_resource.auth_token.user_id)
    user_organizations = []
    for organization in users_organizatons_objects:
        organization = organization.to_dict()
        organization['teams_count'] = get_organization_teams_count(organization['id'])
        organization['users_count'] = get_organization_users_count(organization['id'])
        user_organizations.append(organization)
    return api_resource.response_list_ok(user_organizations, total_count)


@api_bp.route('/users/<uuid:user_id>/organizations', methods=['GET'])
@api_general.rest_api(many=True, access=permissions.PERMISSION__PII_GET_USER_ORGANIZATIONS_LIST)
def pii_get_user_organizations_list(api_resource: ApiResource, user_id: UUID) -> TJsonResponse:
    users_organizatons_objects = get_user_organizations(
        user_id=user_id,
        limit=api_resource.pagination.limit,
        offset=api_resource.pagination.offset,
    )
    total_count = get_user_organizations_count(user_id)
    user_organizations = []
    for organization in users_organizatons_objects:
        organization = organization.to_dict()
        organization['teams_count'] = get_organization_teams_count(organization['id'])
        organization['users_count'] = get_organization_users_count(organization['id'])
        user_organizations.append(organization)
    return api_resource.response_list_ok(user_organizations, total_count)


@api_bp.route('/organizations/<uuid:organization_id>', methods=['GET'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_GET_ORG)
def pii_get_org(api_resource: ApiResource, organization_id: UUID) -> TJsonResponse:
    organization = get_organization_object(organization_id)
    organization = organization.to_dict()
    organization['teams_count'] = get_organization_teams_count(organization['id'])
    organization['users_count'] = get_organization_users_count(organization['id'])
    return api_resource.response_obj_ok(organization)


@api_bp.route('/organizations/current', methods=['GET'])
@api_general.rest_api(many=False, access=api_general.ACCESS_PRIVATE)
def pii_get_current_org(api_resource: ApiResource) -> TJsonResponse:
    organization = get_organization_object(api_resource.auth_token.organization_id)
    organization = organization.to_dict()
    organization['teams_count'] = get_organization_teams_count(organization['id'])
    organization['users_count'] = get_organization_users_count(organization['id'])
    return api_resource.response_obj_ok(organization)


@api_bp.route('/organizations/new', methods=['GET'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_GET_ORG_TPL)
def pii_get_org_tpl(api_resource: ApiResource) -> TJsonResponse:
    organization_fields = get_many_model_fields([Organization, OrganizationData])
    return api_resource.response_obj_ok(organization_fields)


@api_bp.route('/organizations', methods=['POST'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_MK_ORG)
def pii_mk_org(api_resource: ApiResource, body: ApiOrganization) -> TJsonResponse:
    with transaction_commit():
        new_organization = add_new_organization(
            name=body.name,
            admin_notes=body.admin_notes,
            user_created_id=api_resource.auth_token.user_id,
        )
        create_organization_default_teams(
            organization_id=new_organization.id,
            user_created_id=api_resource.auth_token.user_id
        )
    new_organization = new_organization.to_dict()
    new_organization['teams_count'] = get_organization_teams_count(new_organization['id'])
    new_organization['users_count'] = get_organization_users_count(new_organization['id'])
    return api_resource.response_obj_created_ok(new_organization)


@api_bp.route('/organizations/<uuid:organization_id>', methods=['PUT'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_MOD_ORG)
def pii_mod_org(api_resource: ApiResource, body: ApiOrganization, organization_id: UUID) -> TJsonResponse:
    with transaction_commit():
        new_organization = update_organization(
            organization_id=organization_id,
            name=body.name,
            admin_notes=body.admin_notes,
            user_modified_id=api_resource.auth_token.user_id,
        )
    new_organization = new_organization.to_dict()
    new_organization['teams_count'] = get_organization_teams_count(new_organization['id'])
    new_organization['users_count'] = get_organization_users_count(new_organization['id'])
    return api_resource.response_obj_ok(new_organization)


@api_bp.route('/organizations/current', methods=['PUT'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_MOD_CURRENT_ORG)
def pii_mod_current_org(api_resource: ApiResource, body: ApiOrganization) -> TJsonResponse:
    with transaction_commit():
        new_organization = update_organization(
            organization_id=api_resource.auth_token.organization_id,
            name=body.name,
            admin_notes=body.admin_notes,
            user_modified_id=api_resource.auth_token.user_id,
        )
    new_organization = new_organization.to_dict()
    new_organization['teams_count'] = get_organization_teams_count(new_organization['id'])
    new_organization['users_count'] = get_organization_users_count(new_organization['id'])
    return api_resource.response_obj_ok(new_organization)


@api_bp.route('/organizations/<uuid:organization_id>', methods=['DELETE'])
@api_general.rest_api(many=False, access=permissions.PERMISSION__PII_DEL_ORG)
def pii_del_org(api_resource: ApiResource, organization_id: UUID) -> TJsonResponse:
    with transaction_commit():
        delete_organization(
            organization_id=organization_id,
            user_deleted_id=api_resource.auth_token.user_id
        )
    return api_resource.response_obj_deleted_ok()
