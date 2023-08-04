from uuid import UUID, uuid4
from db_utils.modules.db import db

from src.pii__db__general.models.user_credentials_request import UserCredentialsRequest, UserCredentialsRequestType
from src.pii__db__general.helpers.user.get_user import get_user_object
from src.pii__db__general.helpers.check_own_team_org import check_own_team_org


def add_new_user_invite_request(
    user_data_id: UUID,
    organization_id: UUID,
    organization_team_id: UUID,
    user_created_id: UUID
) -> UserCredentialsRequest:
    check_own_team_org(
        organization_id=organization_id,
        organization_team_id=organization_team_id
    )
    new_user_credenetials_request = UserCredentialsRequest(
        id=uuid4(),
        type=UserCredentialsRequestType.invite,
        user_data_id=user_data_id,
        organization_id=organization_id,
        organization_team_id=organization_team_id,
    )
    new_user_credenetials_request.mark_as_created(user_created_id)
    db.session.add(new_user_credenetials_request)
    return new_user_credenetials_request


def add_new_change_password_request(
    user_id: UUID,
    user_created_id: UUID
) -> UserCredentialsRequest:
    get_user_object(user_id)
    new_user_credenetials_request = UserCredentialsRequest(
        id=uuid4(),
        type=UserCredentialsRequestType.change_password,
        user_id=user_id,
        user_data_id=None,
        organization_id=None,
        organization_team_id=None,
    )
    new_user_credenetials_request.mark_as_created(user_created_id)
    db.session.add(new_user_credenetials_request)
    return new_user_credenetials_request


def add_new_reset_password_request(
    user_id: UUID,
    user_created_id: UUID
) -> UserCredentialsRequest:
    get_user_object(user_id)
    new_user_credenetials_request = UserCredentialsRequest(
        id=uuid4(),
        type=UserCredentialsRequestType.reset_password,
        user_id=user_id,
        user_data_id=None,
        organization_id=None,
        organization_team_id=None,
    )
    new_user_credenetials_request.mark_as_created(user_created_id)
    return new_user_credenetials_request
