from datetime import datetime
from enum import Enum
from uuid import uuid4

from db_utils.modules.custom_query import CustomQuery
from db_utils.modules.db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer.serializer import SerializerMixin


class UserAuthLogType(Enum):
    login = 'LOGIN'
    refresh_auth = 'REFRESH_AUTH'


class UserAuthLog(db.Model, SerializerMixin):
    query_class = CustomQuery

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow())
    user_created_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Enum(UserAuthLogType), nullable=False)
    user_agent = db.Column(db.String(1000), nullable=True)
    ipv4 = db.Column(db.String(15), nullable=True)
