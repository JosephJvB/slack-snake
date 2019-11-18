import os
import redis

from base_bot import Base_Bot

class Leaderboard_Bot(Base_Bot):
    def __init__(self):
        super(Leaderboard_Bot, self).__init__()
        redis_url = os.getenv('REDIS_URL')
        if redis_url:
            self.redis = redis.Redis.from_url(redis_url)
        else:
            raise Exception('Redis env vars missing')

    def handle_leaderboard_cmd(self, p):
        self.msg_payload = p
        self.add_react('speech_balloon')
        lb = self.get_leaderboard()
        if len(lb) == 0:
            text = 'Nobody has any points yet!'
        else:
            text = '*Leaderboard:*\n'
            for i, r in enumerate(lb):
                text += f'*{i + 1}.* {r.name}: *{r.points}*\n'
        self.remove_react('speech_balloon')
        self.post_msg(text)
        return

    def handle_points_cmd(self, p):
        self.msg_payload = p
        self.add_react('speech_balloon')
        name = self.get_user_name(p['data']['user'])
        p = int(self.redis.get(name))
        text = f'*{name}* is on *{p}* '
        text += 'point!' if p == 1 else 'points!'
        self.remove_react('speech_balloon')
        self.post_msg(text)

    def get_leaderboard(self):
        keys = self.redis.keys()
        vals = self.redis.mget(keys)
        scores = []
        for i, k in enumerate(keys):
            scores.append({
                'name': k,
                'points': int(vals[i])
            })
        # sort by largest points value > smallest
        scores.sort(key=lambda i: i['points'],
        reverse=True)
        return scores