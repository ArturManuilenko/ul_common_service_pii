from db_utils.modules.custom_query import CustomQuery
from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql.base import UUID

from src.pii__db__general.models.pii_base_user_log_model import PIIBaseUserLogModel


class Organization(PIIBaseUserLogModel):
    __tablename__ = 'organization'

    serialize_rules = ('-organization_data_id', )

    admin_notes = db.Column(db.String(2000))
    organization_data_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization_data.id'), nullable=False)
    organization_data = db.relationship(
        'OrganizationData',
        foreign_keys=[organization_data_id],
        query_class=CustomQuery,
        uselist=False,
    )
