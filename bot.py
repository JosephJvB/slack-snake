import os

who = os.environ['WHOM_CMD']
token = os.environ['BOT_TOKEN']

class Bot:
    def __init__(self):
        print('*****\nbot up\n*****')
        self.guesser_id = None
        self.whomst_id = None
        self.track = None

    # Need to look up what pythons switch statements are like, could be the buzz!!
    def handle_message(self, payload):
        print('hi')
        # payload properties
        web_client = payload['web_client']
        data = payload['data']
        if data.get('bot_profile'):
            # self.handle_bot_message(payload) # not ready!
            return

        print('==========\n')
        print('Message received:')
        print(data)
        # data properies
        channel_id = data['channel']
        content = data['text']
        user = data['user']
        # rtm_client = payload['rtm_client'] # not using rtm_client to respond? Random but sure, you're the boss
        #if 'Hello' in data.get('text', []): # looks like you can try to get a property, and provide a default value, nice!
        is_channel = channel_id == os.environ['CHANNEL_ID']
        is_whom = content.lower().startswith(who) and len(content.split(' ')) > 1
        is_safe = self.whomst_id == None
        mention = [i for i in content.split(' ') if i.startswith('<@') and i.endswith('>')]

        if is_channel and is_whom and is_safe and mention[0]:
            self.guesser_id = user
            self.whomst_id = mention[0]
            # set timeout and reset these propeties
            web_client.chat_postMessage(
                channel=channel_id,
                text='Sick bro, nice hello world bro 😎',
                # thread_ts=data['ts'] # can respond in thread
            )
            # react with speech bubble
        else:
            print('Not respond:')
            print(f'Channel: {channel_id}, text: {content.lower()}')
            print('\n')
        return

    def handle_bot_message(self, payload):
        web_client = payload['web_client']
        data = payload['data']
        channel_id = data['channel']
        content = data['text']
        success = False
        msg_text = ''

        if self.guesser_id and self.whomst_id and content.startswith('This track,'):
            whomst = content.split('<@')[1].replace('>', '')
            if whomst == self.whomst_id:
                success = True
                print('=====\nGUESSED')
                self.track = content.split('This track,')[1].split(', was last requested')[0]
                print(self.guesser_id, self.whomst_id, self.track)
                msg_text = f'<@{self.guesser_id}> You are correct! {self.track} was added by <@{self.whomst_id}>'
                # do some database operation to save success
            else:
                msg_text ='Bad guess!'

            # if success, react check, else react cross
            # web_client.reactions_add(
            #     channel=channel_id,
            #     name='thumbsup',
            # )
            web_client.chat_postMessage(
                channel=channel_id,
                text=msg_text,
            )
            self.reset()
            return

    def reset(self):
        self.whomst_id = None
        self.guesser_id = None
        self.track = None

