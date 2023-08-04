import logging
from datetime import timedelta


class Config(object):
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)

    DELETE_FRESH_EXPIRES = timedelta(days=1)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    JWT_TOKEN_SET_TIME = timedelta(days=1)
    CREDENTIALS_REQUEST_TOKEN_SET_TIME = timedelta(days=1)
