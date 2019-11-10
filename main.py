import os
import slack
from bot import Bot

token = os.environ['BOT_TOKEN']

if not token:
    print('========\nNO BOT TOKEN FOUND')
    print('Exiting...')
else:
    bot = Bot()
    @slack.RTMClient.run_on(event='message')
    def on_message(**payload):
        data = payload['data']
        print('@ on_message', data)
        if not data.get('text') or data['channel'] != os.environ['CHANNEL_ID']:
            return
        elif data.get('bot_profile'):
            bot.handle_bot_message(payload)
        elif data['text'].startswith(os.environ['WHOM_CMD']):
            bot.handle_whom_cmd(payload)
        return

    slack.RTMClient(token=token).start()
