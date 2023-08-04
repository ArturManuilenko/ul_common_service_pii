import json

from src.pii__db__auth.redis_client import redis_client


def store_refresh_token(id: str, ttl: int) -> None:
    redis_client.set(id, json.dumps({}).encode('utf-8'), ttl)


def has_refresh_token(id: str) -> bool:
    return redis_client.exists(id) == 1


def delete_refresh_token(id: str) -> None:
    redis_client.delete(id)
