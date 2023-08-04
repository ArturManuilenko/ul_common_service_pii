from db_utils.modules.db import db
from sqlalchemy.sql.sqltypes import ARRAY, Integer

from src.pii__db__general.models.pii_base_user_log_model import PIIBaseUserLogModel


class BaseOrganizationData(PIIBaseUserLogModel):
    __abstract__ = True

    name = db.Column(db.String(255), nullable=False)
    available_permissions = db.Column(ARRAY(Integer), nullable=False)
