import os
from base_bot import Base_Bot

class Leaderboard_Bot(Base_Bot):
    def __init__(self):
        super(Leaderboard_Bot, self).__init__()
        self.user_prefix = os.getenv('USER_PREFIX')
        self.song_prefix = os.getenv('SONG_PREFIX')

    def handle_user_leaderboard_cmd(self, p):
        self.msg_payload = p
        self.add_react('speech_balloon')
        lb = self.get_leaderboard(self.user_prefix)
        if len(lb) == 0:
            text = 'Nobody has any points yet!'
        else:
            text = '*Leaderboard:*\n'
            for i, r in enumerate(lb):
                text += f'*{i + 1}.* {r["key"]}: *{r["points"]}*\n'
        self.remove_react('speech_balloon')
        self.post_msg(text)
        return

    def handle_user_points_cmd(self, p):
        self.msg_payload = p
        self.add_react('speech_balloon')
        name = self.get_user_name(p['data']['user'])
        p = int(self.redis.get(self.user_prefix+name))
        text = f'*{name}* is on *{p}* '
        text += 'point!' if p == 1 else 'points!'
        self.remove_react('speech_balloon')
        self.post_msg(text)
        return

    def handle_song_leaderboard_cmd(self, p):
        self.msg_payload = p
        self.add_react('speech_balloon')
        lb = self.get_leaderboard(self.song_prefix)
        if len(lb) == 0:
            text = 'No bangers detected!'
        else:
            text = '*Song Leaderboard:*\n'
            for i, r in enumerate(lb):
                text += f'*{i + 1}.* {r["key"]}: *{r["points"]}*\n'
        self.remove_react('speech_balloon')
        self.post_msg(text)
        return

    def get_leaderboard(self, pref):
        keys = self.redis.keys(pref+'*')
        vals = self.redis.mget(keys)
        scores = []
        for i, k in enumerate(keys):
            scores.append({
                'key': k.decode('utf-8').split(pref)[1],
                'points': int(vals[i])
            })
        # sort by largest points value > smallest
        scores.sort(key=lambda i: i['points'],
        reverse=True)
        return scores