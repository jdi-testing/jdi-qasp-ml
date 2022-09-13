import redis

from app import REDIS_PASSWORD, REDIS_HOST

redis_app = redis.Redis(host=REDIS_HOST, port=6379, password=REDIS_PASSWORD)
