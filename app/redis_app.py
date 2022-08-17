import redis

from app import REDIS_PASSWORD

redis_app = redis.Redis(host="redis", port=6379, password=REDIS_PASSWORD)
