import os
import slack
from whom_bot import Whom_Bot
from leaderboard_bot import Leaderboard_Bot

token = os.environ['BOT_TOKEN']

if not token:
    print('========\nNO BOT TOKEN FOUND')
    print('Exiting...')
else:
    whom_bot = Whom_Bot()
    leaderboard_bot = Leaderboard_Bot()
    @slack.RTMClient.run_on(event='message')
    def on_message(**payload):
        data = payload['data']
        print('@ on_message', data)

        if not data.get('text') or data['channel'] != os.environ['CHANNEL_ID']:
            return

        if data.get('bot_profile'):
            t = payload['data']['text']
            whom_bot.handle_bot_message(t)
            return

        if data['text'].startswith(os.environ['WHOM_CMD']):
            whom_bot.handle_whom_cmd(payload)
            return

        if data['text'].startswith(os.environ['LB_CMD']):
            leaderboard_bot.handle_leaderboard_cmd(payload)
            return

        return

    slack.RTMClient(token=token).start()
