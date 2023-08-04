from typing import List
from pydantic import BaseModel, validator
import src.conf.pii__api__general as api_config


class ApiOrganizationTeam(BaseModel):
    name: str
    permissions: List[int]
    is_organization_admin: bool

    @validator('name', allow_reuse=True)
    def check_name_length(cls, value: str) -> str:
        if not api_config.ORGANIZATION_TEAM__NAME__MIN_LENGTH < len(value) < api_config.ORGANIZATION_TEAM__NAME__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.ORGANIZATION_TEAM__NAME__MIN_LENGTH} and less "
                f"then {api_config.ORGANIZATION_TEAM__NAME__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value
