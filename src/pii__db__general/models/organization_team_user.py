from db_utils.modules.custom_query import CustomQuery
from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID

from src.pii__db__general.models.pii_base_user_log_model import PIIBaseUserLogModel


class OrganizationTeamUser(PIIBaseUserLogModel):
    __tablename__ = 'organization_team_user'

    serialize_rules = ('-user_id', '-organization_team_id')

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(
        'User',
        foreign_keys=[user_id],
        query_class=CustomQuery,
        uselist=False,
    )
    organization_team_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization_team.id'), nullable=False)
    organization_team = db.relationship(
        'OrganizationTeam',
        foreign_keys=[organization_team_id],
        query_class=CustomQuery,
        uselist=False,
    )
