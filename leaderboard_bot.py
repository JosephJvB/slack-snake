import random
from threading import Timer
from db import Records
from peewee import fn

from base_bot import Base_Bot

# emoji_dict = {
#     0: ':one:',
#     1: ':two:',
#     2: ':three:',
#     3: ':four:',
#     4: ':five:',
#     5: ':six:',
#     6: ':seven:',
#     7: ':eight:',
#     8: ':nine:',
#     9: ':keycap_ten:',
# }

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
                text += f'*{i + 1}* {r.user}: *{r.count}*\n'
        self.remove_react('speech_balloon')
        self.post_msg(text)
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