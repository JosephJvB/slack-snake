import os
import redis

redis_url = os.getenv('REDIS_URL')
if not redis_url:
    print('bro where ur redis url')
else:
    redis = redis.Redis.from_url(redis_url)
    keys = redis.keys()
    f = open('r-backup.txt', 'w+')
    for key in keys:
        k = key.decode('utf8')
        v = redis.get(k).decode('utf8')
        f.write(f'{k}=joe={v}\n')
    f.close()
    print('migrated ' + str(len(keys)) + ' items')
