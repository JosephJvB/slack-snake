import os
from threading import Timer

who = os.environ['WHOM_CMD']
token = os.environ['BOT_TOKEN']

class Bot:
    def __init__(self):
        print('*****\nbot up\n*****')
        self.msg_payload = None
        self.guesser_id = None
        self.whomst_id = None
        self.track = None

    # Need to look up what pythons switch statements are like, could be the buzz!!
    def handle_whom_cmd(self, payload):
        data = payload['data']
        text = data['text']
        user = data['user']

        mentions = [i for i in text.split(' ') if i.startswith('<@') and i.endswith('>')]

        if not self.msg_payload and len(mentions) > 0:
            self.msg_payload = payload
            self.guesser_id = user
            self.whomst_id = mentions[0]
            print(f'guess received: user={user}, text={text}')
            # react with speech bubble: todo
            Timer(5, self.reset).start() # reset after delay

        return

    def handle_bot_message(self, payload):
        web_client = payload['web_client']
        data = payload['data']
        channel_id = data['channel']
        text = data['text']
        msg_text = ''

        if not self.guesser_id or not self.whomst_id or not text.startswith('This track,'):
            # cases: bot didnt respond in time OR track added in spotify direct
            # remove pending speechbubble reaction from initial message using self.msg_payload
            return

        whomst = text.split('<@')[1].replace('>', '')
        if whomst == self.whomst_id:
            self.track = text.split('This track,')[1].split(', was last requested')[0]
            msg_text = 'Correct!'
            # do database operation to save success
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
        print('\nRESETTING\n')
        self.msg_payload = None
        self.whomst_id = None
        self.guesser_id = None
        self.track = None

