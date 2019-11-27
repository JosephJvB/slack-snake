import requests
import os

from base_bot import Base_Bot

class Banger_Bot(Base_Bot):
    def __init__(self):
        super(Banger_Bot, self).__init__()

    def handle_banger_cmd(self, payload):
        u = 'https://slack.com/api/chat.command'
        d = {
            'channel': os.getenv('BOT_DM'),
            'command': '/whom',
            'token': os.getenv('LEGACY_TOKEN')
        }
        res = requests.post(u, d)
        print(res)
        print(res.text)
        return