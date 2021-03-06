import random
import os
from threading import Timer

from base_bot import Base_Bot

class Whom_Bot(Base_Bot):
    def __init__(self):
        super(Whom_Bot, self).__init__()
        self.msg_user_id = None
        self.guess_user_id = None
        self.actual_user_id = None
        self.locked = False
        self.current_track = None
        self.prefix = os.getenv('USER_PREFIX')

    def handle_whom_cmd(self, p):
        msg_args = p['data']['text'].split(' ')
        if not self.msg_payload and len(msg_args) > 1:
            self.msg_payload = p
            self.msg_user_id = p['data']['user']
            self.guess_user_id = msg_args[1]
            self.add_react('speech_balloon')
            Timer(5, self.reset).start()
        return

    def handle_guess_response(self, text):
        if not text.startswith(':microphone: This track,'):
            return

        self.locked = True
        # one guess per track
        track = text.split('This track, ')[1].split(', was last requested')[0]
        if track != self.current_track:
            self.current_track = track
            self.actual_user_id = text.split('was last requested by ')[1]
            self.respond()
        else:
            self.post_msg(':warning: No double dipping!')

        self.locked = False
        self.reset()
        return

    def respond(self):
        if self.msg_user_id and self.guess_user_id and self.actual_user_id and self.current_track:
            success = self.guess_user_id == self.actual_user_id
            t = self.get_response_text(success)
            r = 'white_check_mark' if success else 'x'
            self.remove_react('speech_balloon')
            self.add_react(r)
            self.post_msg(t)

            if success:
                u = self.get_user_name(self.msg_user_id)
                self.redis.incr(self.prefix + u)
        return

    def reset(self):
        if self.locked: return
        # mayb need to get reactions before removing..if we get errors
        # https://api.slack.com/methods/reactions.get
        print('\nRESETTING\n')
        self.msg_payload = None
        self.msg_user_id = None
        self.guess_user_id = None
        self.actual_user_id = None

    def get_response_text(self, success):
        win_msgs = ['Great job!', 'Correct!', 'Mind reader!', 'Muy epico!', 'Tres bien, mon ami!', '10 outta 10!']
        lose_msgs = ['Better luck next time', 'No way!', 'Not even close!', 'That\'s a no from me', 'Negative on that one']
        l = win_msgs if success else lose_msgs
        return random.choice(l)