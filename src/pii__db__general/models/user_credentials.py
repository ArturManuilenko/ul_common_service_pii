from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.mapper import validates

from src.pii__db__general.models.pii_base_user_log_model import PIIBaseUserLogModel
from src.pii__db__general.modules.hashed_field import BHashedBinary


class UserCredentials(PIIBaseUserLogModel):
    __tablename__ = 'user_credentials'

    serialize_rules = ('-password',)

    login = db.Column(db.String(255), nullable=False)
    password = db.Column(BHashedBinary(), nullable=False)

    date_expiration = db.Column(db.DateTime(), nullable=True)
    user_credentials_request_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user_credentials_request.id"), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    @validates('password')
    def validate_and_hash_password(self, key: str, password: str) -> str:
        if not len(password) > 6:
            raise ValueError('Password length must be more then 6 symbols')
        if len(password) > 255:
            raise ValueError('Password length must be less then 255 symbols')
        return password
