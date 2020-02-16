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
        args = p['data']['text'].split(' ')
        if len(args) < 2: # todo: barry without userid returns current barry
            return
        barry_id = args[1].replace('<@', '').replace('>', '').split('|')[0] # get user id from message !barry @user
        prev = self.redis.get(_prefix)
        self.redis.set(_prefix, barry_id) # set new barry
        if prev: # handle prev
            prev = prev.decode('utf8')
            self.redis.set(_prefix, barry_id)
            p_user = self.try_get_user(prev)
            p_username = ''
            if p_user['profile'].get('display_name'):
                p_username = p_user['profile']['display_name']
            elif p_user['profile'].get('first_name'):
                p_username = p_username = p_user['profile']['first_name']
            else:
                p_username = p_user['profile'].get('real_name')
            self.set_display_name(prev, p_username)

        updated_name = '[BARRY] ' # update new barry name
        u = self.try_get_user(barry_id)
        print(u)
        if u['profile'].get('display_name'):
            updated_name += u['profile']['display_name']
        elif u['profile'].get('first_name'):
            updated_name += u['profile']['first_name']
        else:
            updated_name += u['profile'].get('real_name')
        self.set_display_name(barry_id, updated_name)
        print(f'set new barry: {updated_name}')
        return