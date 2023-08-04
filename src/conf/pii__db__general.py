import os
from db_utils.modules.db import DbConfig


db_config = DbConfig(
    uri=os.environ['PII__DB__GENERAL__DB_URI'],
    track_mod=False
)

PII__DB__GENERAL__SYS_USER_ID = os.environ['PII__DB__GENERAL__SYS_USER_ID']
PII__DB__GENERAL__GUEST_USER_ID = os.environ['PII__DB__GENERAL__GUEST_USER_ID']
PII__DB__GENERAL__ADMIN_USER_ID = os.environ['PII__DB__GENERAL__ADMIN_USER_ID']
