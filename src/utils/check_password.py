from bcrypt import checkpw


def check_password(request_password: bytes, db_password: bytes) -> bool:
    if not isinstance(request_password, bytes):
        request_password = bytes(request_password, 'utf8')
    if not isinstance(db_password, bytes):
        request_password = bytes(db_password, 'utf8')
    return checkpw(request_password, db_password)
