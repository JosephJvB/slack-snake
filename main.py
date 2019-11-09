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
        bot.handle_message(payload)
        return

    slack.RTMClient(token=token).start()
