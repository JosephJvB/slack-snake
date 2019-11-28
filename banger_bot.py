import os
import requests

from base_bot import Base_Bot

class Banger_Bot(Base_Bot):
    def __init__(self):
        super(Banger_Bot, self).__init__()
        self.song_prefix = os.getenv('SONG_PREFIX')
        self.user_prefix = os.getenv('USER_PREFIX')
        self.banger = None
        self.banged_by = []


    def handle_banger_cmd(self, payload):
        self.msg_payload = payload
        u = 'https://slack.com/api/chat.command'
        d = {
            'channel': os.getenv('DM_ID'),
            'command': '/whom',
            'token': os.getenv('LEGACY_TOKEN')
        }
        requests.post(u, d)
        return
    
    def handle_banger_response(self, text):
        if text.startswith(':microphone: This track,'):
            user_id = text.split('was last requested by ')[1].split('<@')[1].split('|')[0]
            # cant bang your own tracks
            if user_id == self.msg_payload['data']['user']:
                self.post_msg('Please don\'t try to bang yourself at work...:nauseated_face:')
            else:
                name = self.get_user_name(user_id)
                track = text.split('This track, ')[1].split(', was last requested')[0]
                # reset on new track
                if name and track:
                    if self.banger != track:
                        self.banger = track
                        self.banged_by = []
                    # only bang once
                    if name not in self.banged_by:
                        self.post_msg(f':rotating_light: BANGER ALERT: "{track}" :rotating_light:')
                        self.redis.incr(self.song_prefix + track)
                        self.redis.incr(self.user_prefix + name)
                        self.banged_by.append(name)
                    else:
                        self.post_msg(':warning: No double dipping!')
        self.msg_payload = None
        return