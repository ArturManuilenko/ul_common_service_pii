from typing import Tuple
from uuid import UUID

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID as pgUUID      # noqa: N811 UUID is not constant, allow to associating
from db_utils.model.base_user_log_model import BaseUserLogModel
from db_utils.modules.db import db


class PIIBaseUserLogModel(BaseUserLogModel):
    """Redefinition BaseUserLogModel with foreign keys to User model"""
    __abstract__ = True

    @declared_attr
    def user_created_id(self) -> Tuple[UUID, str]:
        return db.Column(pgUUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    @declared_attr
    def user_modified_id(self) -> Tuple[UUID, str]:
        return db.Column(pgUUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    @declared_attr
    def user_deleted_id(self) -> Tuple[UUID, str]:
        return db.Column(pgUUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
