import json
import secrets
from uuid import UUID, uuid4
from src.pii__db__auth.redis_client import redis_client
from api_utils.errors.api_no_result_found import ApiNoResultFoundError


def generate_xor() -> str:
    xor = secrets.token_urlsafe(255)
    return xor


def store_xor_token(xor_token: str) -> UUID:
    uuid_key = uuid4()
    redis_client.set(str(uuid_key), json.dumps({'xor_token': str(xor_token)}).encode('utf-8'), 300)
    return uuid_key


def get_xor_token(xor_key_id: UUID) -> str:
    value = redis_client.get(str(xor_key_id))
    if not value:
        raise ApiNoResultFoundError('session-token not valid')
    xor_key = json.loads(value)['xor_token']
    redis_client.delete(str(xor_key_id))
    return xor_key
