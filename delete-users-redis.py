import os
import redis

redis_url = os.getenv('REDIS_URL')
if not redis_url:
    print('bro where ur redis url')
else:
    redis = redis.Redis.from_url(redis_url)
    keys = redis.keys()
    for key in keys:
        k = key.decode('utf8')
        if k.startswith('user:'):
            redis.set(k, 0)
    print('reset ' + str(len(keys)) + ' user records')
