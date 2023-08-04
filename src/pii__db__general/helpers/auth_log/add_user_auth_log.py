
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from db_utils.modules.db import db

from src.pii__db__general.models.user_auth_log import UserAuthLog, UserAuthLogType


def add_user_auth_log(
    type: UserAuthLogType,
    user_id: UUID,
    user_created_id: UUID,
    user_agent: Optional[str],
    ipv4: Optional[str]
) -> UserAuthLog:
    new_user_auth_log = UserAuthLog(
        id=uuid4(),
        date_created=datetime.utcnow(),
        user_created_id=user_created_id,
        type=type,
        user_id=user_id,
        user_agent=user_agent,
        ipv4=ipv4
    )
    db.session.add(new_user_auth_log)
    return new_user_auth_log
