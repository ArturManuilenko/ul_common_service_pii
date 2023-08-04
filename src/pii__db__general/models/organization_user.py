from enum import Enum

from db_utils.modules.custom_query import CustomQuery
from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID

from src.pii__db__general.models.pii_base_user_log_model import PIIBaseUserLogModel


class OrganizationUserState(Enum):
    active = "ACTIVE"
    blocked = "BLOCKED"


class OrganizationUser(PIIBaseUserLogModel):
    __tablename__ = 'organization_user'
    __table_args__ = tuple(
        db.UniqueConstraint('organization_id', 'user_id')
    )

    serialize_rules = ('-organization_id', )

    notes = db.Column(db.String(1000), nullable=False)
    state = db.Column(db.Enum(OrganizationUserState), nullable=False)

    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    organization = db.relationship(
        'Organization',
        foreign_keys=[organization_id],
        query_class=CustomQuery,
        uselist=False,
    )
    user = db.relationship(
        'User',
        foreign_keys=[user_id],
        query_class=CustomQuery,
        uselist=False,
    )
