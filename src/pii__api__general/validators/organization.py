from typing import Optional
from pydantic import BaseModel, validator
import src.conf.pii__api__general as api_config


class ApiOrganization(BaseModel):       # ellipses in default for check field key requeired with optional value
    admin_notes: Optional[str] = ...    # type: ignore
    name: str                           # mypy 0.812 not don't understaned this pydantic developers feature

    @validator('admin_notes', allow_reuse=True)
    def check_admin_notes_length(cls, value: str) -> str:
        if not api_config.ORGANIZATION__ADMIN_NOTES__MIN_LENGTH < len(
                value) < api_config.ORGANIZATION__ADMIN_NOTES__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.ORGANIZATION__ADMIN_NOTES__MIN_LENGTH} and less "
                f"then {api_config.ORGANIZATION__ADMIN_NOTES__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value

    @validator('name', allow_reuse=True)
    def check_name_length(cls, value: str) -> str:
        if not api_config.ORGANIZATION_DATA__NAME__MIN_LENGTH < len(
                value) < api_config.ORGANIZATION_DATA__NAME__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.ORGANIZATION_DATA__NAME__MIN_LENGTH} and less "
                f"then {api_config.ORGANIZATION_DATA__NAME__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value
