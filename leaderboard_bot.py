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
            for i, r in enumerate(query_results[:10]):
                text += f'{self.get_emoji(i)} {r.user}: *{r.count}*\n'
        self.remove_react('speech_balloon')
        self.post_msg(text)
        return

    def get_emoji(self, n):
        if n == 0: return ':one:'
        if n == 1: return ':two:'
        if n == 2: return ':three:'
        if n == 3: return ':four:'
        if n == 4: return ':five:'
        if n == 5: return ':six:'
        if n == 6: return ':seven:'
        if n == 7: return ':eight:'
        if n == 8: return ':nine:'
        if n == 9: return ':keycap_ten:'
        return

    def handle_points_cmd(self, p):
        self.msg_payload = p
        self.add_react('speech_balloon')
        name = self.get_user_name(p['data']['user'])
        query_results = (Records.select(Records.user, fn.COUNT('*')
            .alias('count'))
            .where(Records.user==name))
        p = query_results[0].count
        text = f'*{name}* is on *{p}* '
        text += 'point!' if p == 1 else 'points!'
        self.remove_react('speech_balloon')
        self.post_msg(text)