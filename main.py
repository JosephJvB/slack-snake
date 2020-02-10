import os
import slack
from threading import Thread
from datetime import datetime
import time

from whom_bot import Whom_Bot
from leaderboard_bot import Leaderboard_Bot
from banger_bot import Banger_Bot
from bamboo_bot import Bamboo_Bot

token = os.environ['BOT_TOKEN']

if not token:
    print('========\nNO BOT TOKEN FOUND')
    print('Exiting...')
else:
    whom_bot = Whom_Bot()
    leaderboard_bot = Leaderboard_Bot()
    banger_bot = Banger_Bot()
    bamboo_bot = Bamboo_Bot()

    CMDS = {
        os.environ['POINTS_CMD']: leaderboard_bot.handle_user_points_cmd,
        os.environ['WHOM_CMD']: whom_bot.handle_whom_cmd,
        os.environ['LB_CMD']: leaderboard_bot.handle_user_leaderboard_cmd,
        os.environ['SONG_LB_CMD']: leaderboard_bot.handle_song_leaderboard_cmd,
        os.environ['BANGER_CMD']: banger_bot.handle_banger_cmd,
        # os.environ['TIMEOFF_CMD']: bamboo_bot.handle_timeoff_cmd,
    }

    @slack.RTMClient.run_on(event='message')
    def on_message(**payload):
        data = payload['data']
        print('@ on_message', data)

        if data.get('bot_profile'): 
            t = payload['data']['text']
            if data['channel'] == os.environ['CHANNEL_ID']:
                whom_bot.handle_guess_response(t)
                return

            if data['channel'] == os.environ['DM_ID']:
                banger_bot.handle_dm_response(t)
                return

        # maybe each command should handle their own channels
        if not data.get('text') or data['channel'] != os.environ['CHANNEL_ID']:
            return

        cmd = data['text'].split(' ')[0]
        handler = CMDS.get(cmd)
        if handler:
            handler(payload)
        return

    def cron_job(): # 7.45pm UTC == 8.45am NZT
        timeout = 60 * 60

        while True:
            if datetime.utcnow().hour > 17:
                timeout = 60 * 15

            if datetime.utcnow().hour == 19:
                timeout = 60 * 5
                if datetime.utcnow().minute > 35:
                    bamboo_bot.check_anniversaries()
                    timeout = 60 * 60 * 20 # after done, sleep for 20 hrs

            time.sleep(timeout)

    Thread(target=cron_job, daemon=True).start()
    slack.RTMClient(token=token).start()
