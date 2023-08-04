from src.utils.invalid_credentials_error import invalid_credentials_error


def xor_unxor(data: str, xor_token: str) -> str:
    result = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(data, xor_token))
    return result


def unhex_credentials(data: str) -> str:
    try:
        credentials = bytes.fromhex(data).decode('utf-8')
    except ValueError:
        invalid_credentials_error()
    return credentials


def decrypt_credentials(credentials: str, token: str) -> str:
    unhexed_credentials = unhex_credentials(credentials)
    unxored_credentials = xor_unxor(unhexed_credentials, token)
    return unxored_credentials
