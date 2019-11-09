import os
import slack

if not os.environ['BOT_TOKEN']:
    print('NO BOT TOKEN FOUND')
    print('Exiting...')
else:
    @slack.RTMClient.run_on(event='message')
    def on_message(**payload):
        data = payload['data']
        if data.get('bot_profile'): return
        print('==========\n')
        print('Message received:')
        print(data)
        # data properies
        channel_id = data['channel']
        web_client = payload['web_client']
        content = data['text']
        user = data['user']
        # rtm_client = payload['rtm_client'] # not using rtm_client to respond? Random but sure, you're the boss
        #if 'Hello' in data.get('text', []): # looks like you can try to get a property, and provide a default value, nice!
        should_respond = channel_id == os.environ['CHANNEL_ID'] and content.lower().startswith(os.environ['WHOM_CMD'])
        if should_respond:
            web_client.chat_postMessage(
                channel=channel_id,
                text=f'Whom?? It\'s me silly!!!! hahahaha',
                # thread_ts=data['ts'] # can respond in thread
            )
        else:
            print('Not respond:')
            print(f'Channel: {channel_id}, text: {content.lower()}')
            print('\n')
        return

    slack_token = os.environ['BOT_TOKEN']
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()