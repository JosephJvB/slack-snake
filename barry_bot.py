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