import os
from db import Records
from peewee import fn
import redis

def main():
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        c = redis.Redis.from_url(redis_url)
        query_results = Records.select(Records.user)
        for r in query_results:
            print(r.user)
            c.incr(r.user)
    else:
        raise Exception('Redis env vars missing')

if __name__ == '__main__': main()