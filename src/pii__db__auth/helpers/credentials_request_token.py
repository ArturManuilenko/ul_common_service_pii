import json
from typing import Optional
from uuid import UUID

from src.pii__db__auth.redis_client import redis_client


def store_credentials_request_token(
    credentials_request_id: UUID,
    credentials_request_token: str,
    ttl: int
) -> None:
    redis_client.set(
        name=credentials_request_token,
        value=json.dumps({"credentials_request_id": str(credentials_request_id)}).encode('utf-8'),
        ex=ttl
    )
    # write key: token too TEMPORARY, before email notification system
    redis_client.set(
        name=str(credentials_request_id),
        value=json.dumps({"credentials_request_token": str(credentials_request_token)}).encode('utf-8'),
        ex=ttl
    )


def get_credentials_request_id(token: str) -> Optional[str]:
    return json.loads(redis_client.get(token)).get('credentials_request_id', None)


def has_credentials_request_token(id: str) -> bool:
    return redis_client.exists(id) == 0


def delete_credentials_request_token(id: str) -> None:
    redis_client.delete(id)
