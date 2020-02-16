"""
send command to bot
!barry @user
lookup prev barry, if exist: 
    - remove prev barry from user.display_name
    - remove prev barry from redis
- add user
Update users name as [BARRY] "name"

api to update users name on slack
https://github.com/slackapi/python-slackclient/blob/master/slack/web/client.py#L1687
https://api.slack.com/methods/users.profile.set

call set profile with body:
updated_name = '[BARRY] '
if user.display_name:
    updated_name += user.display_name
elif user.first_name:
    updated_name += user.user.first_name
elif user.real_name:
    updated_name += user.user.real_name
{
    'token': 'Bearer <token>', try without this first
    'name': 'display_name'
    'value': f'[BARRY] {user.first_name}'
}
"""
import os
import requests

from base_bot import Base_Bot

_prefix = '_barry:'

class Barry_Bot(Base_Bot):
    def __init__(self):
        super(Barry_Bot, self).__init__()
        self.banger = None
        self.banged_by = []

    def handle_barry_cmd(self, p):
        self.msg_payload = p
        # find user by id in message
        args = p['data']['text'].split(' ')
        if len(args) < 1: # todo: barry without userid returns current barry
            return
        barry_id = args[1].replace('<@', '').replace('>', '')
        prev = self.redis.get(_prefix)
        if prev:
            self.redis.set(_prefix, barry_id)
            p_user = self.get_user(prev)
            p_username = 'wip'

        updated_name = '[BARRY]' # handle new barry
            u = self.get_user(user_id)
            if u.display_name:
                updated_name += u.display_name
            elif u.first_name:
                updated_name += u.user_first_name
            elif u.real_name:
                updated_name += u.user_real_name
        return