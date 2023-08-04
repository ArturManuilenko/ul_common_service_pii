from db_utils.modules.db import db
from sqlalchemy import ARRAY, Integer

from src.pii__db__general.models.pii_base_user_log_model import PIIBaseUserLogModel


class BaseOrganizationTeam(PIIBaseUserLogModel):
    __abstract__ = True

    name = db.Column(db.String(255), nullable=False)
    permissions = db.Column(ARRAY(Integer), nullable=False)
    is_organization_admin = db.Column(db.Boolean(), nullable=False)
    is_system = db.Column(db.Boolean(), default=False, nullable=False)
