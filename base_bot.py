import os
import redis

class Base_Bot(object):
    def __init__(self):
        redis_url = os.getenv('REDIS_URL')
        if redis_url:
            self.redis = redis.Redis.from_url(redis_url)
            self.msg_payload = None
        else:
            raise Exception('Redis env vars missing')

    def post_msg(self, text):
        if self.msg_payload is None:
            print('post_msg: msg_payload not set!')
        else:
            self.msg_payload['web_client'].chat_postMessage(
                channel=self.msg_payload['data']['channel'],
                timestamp=self.msg_payload['data']['ts'],
                text=text)
        return

    def add_react(self, name):
        if self.msg_payload is None:
            print('add_react: msg_payload not set!')
        else:
            self.msg_payload['web_client'].reactions_add(
                name=name,
                channel=self.msg_payload['data']['channel'],
                timestamp=self.msg_payload['data']['ts'])
        return

    def remove_react(self, name):
        if self.msg_payload is None:
            print('remove_react: msg_payload not set!')
        else:
            self.msg_payload['web_client'].reactions_remove(
                name=name,
                channel=self.msg_payload['data']['channel'],
                timestamp=self.msg_payload['data']['ts'])
        return

    def get_user_name(self, user_id):
        if self.msg_payload is None:
            print('get_user: msg_payload not set!')
        else:
            res = self.msg_payload['web_client'].users_info(user=user_id)
            return res['user']['real_name']
