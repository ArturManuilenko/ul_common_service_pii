from api_utils.errors.api_validate_error import ApiValidateError


def invalid_credentials_error() -> None:
    raise ApiValidateError(
        code='login/password_error',
        location=['password, login'],
        msg_template='wrong combination of login/password',
    )
