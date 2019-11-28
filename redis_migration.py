import os
import redis

# user:USERNAME = userscore
# so I can use
# song:SONGNAME = songscore

redis_url = os.getenv('REDIS_URL')
if not redis_url:
    print('bro where ur redis url')
else:
    redis = redis.Redis.from_url(redis_url)
    keys = redis.keys()
    for key in keys:
        k = key.decode('utf8')
        if not k.startswith('user:'):
            v = redis.get(k)
            redis.set('user:' + k, v)
            redis.delete(k)
    print('migrated ' + str(len(keys)) + ' items')
