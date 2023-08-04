import re
from typing import Optional, Union
from pydantic import BaseModel, validator
from pydantic.types import UUID4
import src.conf.pii__api__general as api_config


class ApiUser(BaseModel):                           # ellipses in default for check field key requeired with optional value
    email: str                                      # mypy 0.812 not don't understaned this pydantic developers feature
    about: Optional[str] = ...                      # type: ignore
    admin_notes: Optional[str] = ...                # type: ignore
    nick_name: Optional[str] = ...                  # type: ignore
    first_name: Optional[str] = ...                 # type: ignore
    last_name: Optional[str] = ...                  # type: ignore
    middle_name: Optional[str] = ...                # type: ignore
    avatar_media_file_id: Union[UUID4, None] = ...  # type: ignore

    @validator('admin_notes', allow_reuse=True)
    def check_admin_notes_length(cls, value: str) -> str:
        if value and not api_config.USER__MIN_ADMIN_NOTES_LENGTH < len(value) < api_config.USER__MAX_ADMIN_NOTES_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.USER__MIN_ADMIN_NOTES_LENGTH} and less "
                f"then {api_config.USER__MAX_ADMIN_NOTES_LENGTH} symbols, get {len(value)}",
            )
        return value

    @validator('email', allow_reuse=True)
    def check_email_length(cls, value: str) -> str:
        if not api_config.USER_DATA__EMAIL__MIN_LENGTH < len(value) < api_config.USER_DATA__EMAIL__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.USER_DATA__EMAIL__MIN_LENGTH} and less "
                f"then {api_config.USER_DATA__EMAIL__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value

    @validator('email', allow_reuse=True)
    def check_valid_email(cls, value: str) -> str:
        if not re.match(api_config.USER_DATA__EMAIL__REGEX, value):
            raise ValueError("invalid email format")
        return value

    @validator('nick_name', allow_reuse=True)
    def check_nick_name_length(cls, value: str) -> str:
        if value and not api_config.USER_DATA__NICK_NAME__MIN_LENGTH < len(value) < api_config.USER_DATA__NICK_NAME__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.USER_DATA__NICK_NAME__MIN_LENGTH} and less "
                f"then {api_config.USER_DATA__NICK_NAME__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value

    @validator('first_name', allow_reuse=True)
    def check_first_name_length(cls, value: str) -> str:
        if value and not api_config.USER_DATA__FIRST_NAME__MIN_LENGTH < len(value) < api_config.USER_DATA__FIRST_NAME__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.USER_DATA__FIRST_NAME__MIN_LENGTH} and less "
                f"then {api_config.USER_DATA__FIRST_NAME__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value

    @validator('last_name', allow_reuse=True)
    def check_last_name_length(cls, value: str) -> str:
        if value and not api_config.USER_DATA__LAST_NAME__MIN_LENGTH < len(value) < api_config.USER_DATA__LAST_NAME__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.USER_DATA__LAST_NAME__MIN_LENGTH} and less "
                f"then {api_config.USER_DATA__LAST_NAME__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value

    @validator('middle_name', allow_reuse=True)
    def check_middle_name_length(cls, value: str) -> str:
        if value and not api_config.USER_DATA__MIDDLE_NAME__MIN_LENGTH < len(value) < api_config.USER_DATA__MIDDLE_NAME__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.USER_DATA__MIDDLE_NAME__MIN_LENGTH} and less "
                f"then {api_config.USER_DATA__MIDDLE_NAME__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value

    @validator('about', allow_reuse=True)
    def check_about_length(cls, value: str) -> str:
        if value and not api_config.USER_DATA__ABOUT__MIN_LENGTH < len(value) < api_config.USER_DATA__ABOUT__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.USER_DATA__ABOUT__MIN_LENGTH} and less "
                f"then {api_config.USER_DATA__ABOUT__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value
