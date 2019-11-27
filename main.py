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

    CMDS = {
        os.environ['POINTS_CMD']: leaderboard_bot.handle_points_cmd,
        os.environ['WHOM_CMD']: whom_bot.handle_whom_cmd,
        os.environ['LB_CMD']: leaderboard_bot.handle_leaderboard_cmd,
        os.environ['BANGER_CMD']: whom_bot.handle_banger_cmd,
    }

    @slack.RTMClient.run_on(event='message')
    def on_message(**payload):
        data = payload['data']
        print('@ on_message', data)

        if data.get('bot_profile'): 
            # how to handle /whom from user as guess
            # AND handle /whom from bot and await response
            if data['channel'] == os.environ['CHANNEL_ID']:
                t = payload['data']['text']
                whom_bot.handle_bot_message(t)
            return

        if not data.get('text') or data['channel'] != os.environ['CHANNEL_ID']:
            return


        cmd = data['text'].split(' ')[0]
        handler = CMDS.get(cmd)
        if handler:
            handler(payload)

        return

    slack.RTMClient(token=token).start()
