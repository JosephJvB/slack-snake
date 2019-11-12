import random
from threading import Timer
from db import Records
from peewee import fn

from base_bot import Base_Bot

class Leaderboard_Bot(Base_Bot):
    def __init__(self):
        super(Leaderboard_Bot, self).__init__()

    def handle_leaderboard_cmd(self, p):
        self.msg_payload = p
        self.add_react('speech_balloon')
        query_results = (Records.select(Records.user, fn.COUNT('*')
            .alias('count'))
            .group_by(Records.user)
            .order_by(fn.COUNT('*').alias('count').desc()))
        if len(query_results) == 0:
            text = 'Nobody has any points yet!'
        else:
            text = '*Leaderboard:*\n'
            for i, r in enumerate(query_results[:3]):
                text += f'{self.get_medal(i)} <@{r.user}>: *{r.count}*\n'
        self.remove_react('speech_balloon')
        self.post_msg(text)
        return

    def get_medal(self, n):
        if n == 0: return ':first_place_medal:'
        if n == 1: return ':second_place_medal:'
        if n == 2: return ':third_place_medal:'
        return