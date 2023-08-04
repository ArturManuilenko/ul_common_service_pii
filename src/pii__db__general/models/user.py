from db_utils.modules.custom_query import CustomQuery
from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID

from src.pii__db__general.models.pii_base_user_log_model import PIIBaseUserLogModel


class User(PIIBaseUserLogModel):
    __tablename__ = 'user'

    serialize_rules = ('-user_data_id', '-organization_user.user')

    is_system = db.Column(db.Boolean(), default=False, nullable=False)
    user_data_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_data.id'), nullable=False)
    user_data = db.relationship(
        "UserData",
        foreign_keys=[user_data_id],
        query_class=CustomQuery,
        uselist=False,
    )
    organizations = db.relationship(
        "Organization",
        secondary="organization_user",
        primaryjoin="Organization.id == OrganizationUser.organization_id",
        secondaryjoin="OrganizationUser.user_id == User.id",
        query_class=CustomQuery,
        uselist=True,
        viewonly=True
    )
    last_auth_log = db.relationship(
        "UserAuthLog",
        lazy="joined",
        primaryjoin="UserAuthLog.user_id == User.id",
        order_by="UserAuthLog.date_created.desc()",
        uselist=False,
    )

    organization_user = db.relationship(
        "OrganizationUser",
        primaryjoin="OrganizationUser.user_id == User.id",
    )
