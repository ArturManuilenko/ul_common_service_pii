from uuid import UUID

from api_utils.api_resource.api_resource import ApiResource
from api_utils.utils.constants import TJsonResponse
from db_utils import transaction_commit

import src.conf.permissions as permissions  # noqa: F401
from src.pii__api__general.routes import api_bp
from src.conf.pii__api__general import api_general
from src.pii__api__general.validators.organization_user import ApiOrganizationUser
from src.pii__db__general.helpers.organization_user.update_organization_user import \
    update_organization_user_obj


@api_bp.route('/organization/<uuid:organization_id>/users/<uuid:user_id>', methods=["PATCH"])
@api_general.rest_api(many=False, access=api_general.ACCESS_PUBLIC)
def pii_add_user_to_current_org_team(
        api_resource: ApiResource,
        body: ApiOrganizationUser,
        organization_id: UUID,
        user_id: UUID,
) -> TJsonResponse:
    with transaction_commit():
        organization_user = update_organization_user_obj(
            organization_id=organization_id,
            user_id=user_id,
            user_modified_id=api_resource.auth_token.user_id,
            notes=body.notes,
            state=body.state,
        )
    return api_resource.response_obj_created_ok(organization_user.to_dict())
