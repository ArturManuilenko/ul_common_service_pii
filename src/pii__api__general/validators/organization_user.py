from pydantic import BaseModel, validator
import src.conf.pii__api__general as api_config
from src.pii__db__general.models.organization_user import OrganizationUserState


class ApiOrganizationUser(BaseModel):
    notes: str
    state: OrganizationUserState

    @validator('notes', allow_reuse=True)
    def check_name_length(cls, value: str) -> str:
        if not api_config.ORGANIZATION_USER__NOTES__MIN_LENGTH < len(value) < api_config.ORGANIZATION_USER__NOTES__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.ORGANIZATION_USER__NOTES__MIN_LENGTH} and less "
                f"then {api_config.ORGANIZATION_USER__NOTES__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value
