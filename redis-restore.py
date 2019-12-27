import os
import redis

redis_url = os.getenv('REDIS_URL')
if not redis_url:
    print('bro where ur redis url')
else:
    redis = redis.Redis.from_url(redis_url)
    f = open('r-backup.txt')
    lines = f.readlines()
    for l in lines:
        k, v = l.split('=joe=')
        redis.set(k, v)
    f.close()
    print('inserted ' + str(len(lines)) + ' items')
