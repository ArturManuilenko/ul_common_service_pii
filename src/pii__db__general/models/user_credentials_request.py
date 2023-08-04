from enum import Enum

from db_utils.modules.custom_query import CustomQuery
from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID

from src.pii__db__general.models.pii_base_user_log_model import PIIBaseUserLogModel


class UserCredentialsRequestType(Enum):
    invite = 'INVITE'
    reset_password = 'RESET_PASSWORD'
    change_password = 'CHANGE_PASSWORD'


class UserCredentialsRequest(PIIBaseUserLogModel):
    __tablename__ = 'user_credentials_request'

    serialize_rules = ('-user_data_id', )

    type = db.Column(db.Enum(UserCredentialsRequestType), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
    user_data_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_data.id'), nullable=True)
    user_data = db.relationship(
        "UserData",
        foreign_keys=[user_data_id],
        query_class=CustomQuery,
        uselist=False,
    )
    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization.id'), nullable=True)
    organization_team_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization_team.id'), nullable=True)
    date_confirmed = db.Column(db.DateTime(), nullable=True)
