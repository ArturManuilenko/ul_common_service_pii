from db_utils import CustomQuery
from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID

from src.pii__db__general.models.base_organization_team import BaseOrganizationTeam


class OrganizationTeam(BaseOrganizationTeam):
    __tablename__ = 'organization_team'

    serialize_rules = ('-organization_id', )

    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization.id'), nullable=False)
    organization = db.relationship(
        'Organization',
        foreign_keys=[organization_id],
        query_class=CustomQuery,
        uselist=False,
    )
