import redis
from app.config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def acquire_lock(slot_key: str):
    return r.set(slot_key, "locked", nx=True, ex=30)