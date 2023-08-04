from pydantic import BaseModel, validator
import src.conf.pii__api__general as api_config


class ApiUserCredentials(BaseModel):
    login: str
    password: str

    @validator('login', allow_reuse=True)
    def check_login_length(cls, value: str) -> str:
        if not api_config.USER_CREDENTIALS__LOGIN__MIN_LENGTH < len(value) < api_config.USER_CREDENTIALS__LOGIN__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.USER_CREDENTIALS__LOGIN__MIN_LENGTH} and less "
                f"then {api_config.USER_CREDENTIALS__PASSWORD__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value

    @validator('password', allow_reuse=True)
    def check_password_length(cls, value: str) -> str:
        if not api_config.USER_CREDENTIALS__PASSWORD__MIN_LENGTH < len(value) < api_config.USER_CREDENTIALS__PASSWORD__MAX_LENGTH:
            raise ValueError(
                f"length must be more then {api_config.USER_CREDENTIALS__PASSWORD__MIN_LENGTH} and less "
                f"then {api_config.USER_CREDENTIALS__PASSWORD__MAX_LENGTH} symbols, get {len(value)}"
            )
        return value
