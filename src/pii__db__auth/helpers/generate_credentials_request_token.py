from secrets import token_urlsafe


def generate_credentials_request_token() -> str:
    return token_urlsafe()
