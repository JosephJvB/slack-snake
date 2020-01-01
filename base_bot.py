import os
import redis
import requests

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
        u = self.get_user_by_id(user_id)
        return u['user']['real_name']

    def get_user_by_id(self, user_id):
        if self.msg_payload is None:
            print('get_user: msg_payload not set!')
        else:
            res = self.msg_payload['web_client'].users_info(user=user_id)
            return res

    def send_cmd(self, cmd, channel, args=None):
        u = 'https://slack.com/api/chat.command'
        d = {
            'channel': channel,
            'command': cmd,
            'token': os.getenv('LEGACY_TOKEN'),
            'text': args
        }
        requests.post(u, d)
        return
