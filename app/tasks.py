import json

from redis.client import Redis
from redis.lock import Lock

from app.celery_app import celery_app
from utils.robula import generate_xpath


@celery_app.task
def task_xpath_generation():
    with Redis('redis') as redis:
        with Lock(redis, "priority_lock"):
            keys = sorted((int(e) for e in redis.hkeys("priority_queue")))
            for top_priority in keys:
                queue = json.loads(redis.hget("priority_queue", top_priority))
                if queue:
                    top_priority_task = queue.pop()
                    redis.hset("priority_queue", top_priority, json.dumps(queue))
                    break
                redis.hdel("priority_queue", top_priority)

        element_id, document, config = top_priority_task
        result = generate_xpath(element_id, document, config)
        redis.hset("generated_xpaths", element_id, result)

    return result
