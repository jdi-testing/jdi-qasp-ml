import redis

from app import REDIS_HOST, REDIS_PASSWORD

redis_app = redis.Redis(host=REDIS_HOST, port=6379, password=REDIS_PASSWORD)
