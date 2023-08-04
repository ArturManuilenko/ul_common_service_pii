import redis

from src.conf.pii__db__auth import PII__DB__AUTH__DB_URI

redis_client = redis.StrictRedis(PII__DB__AUTH__DB_URI)
