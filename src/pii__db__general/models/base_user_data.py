from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID

from src.pii__db__general.models.pii_base_user_log_model import PIIBaseUserLogModel


class BaseUserData(PIIBaseUserLogModel):
    __abstract__ = True

    email = db.Column(db.String(255), nullable=False)
    nick_name = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    middle_name = db.Column(db.String(255), nullable=True)
    avatar_media_file_id = db.Column(UUID(as_uuid=True), nullable=True)
    admin_notes = db.Column(db.String(1000), nullable=True)
    about = db.Column(db.String(1000), nullable=True)
