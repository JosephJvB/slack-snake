import os
from threading import Timer

who = os.environ['WHOM_CMD']
token = os.environ['BOT_TOKEN']

class Bot:
    def __init__(self):
        print('*****\nbot up\n*****')
        self.msg_payload = None
        self.msg_user_id = None
        self.guess_user_id = None
        self.actual_user_id = None
        self.track = None

    def handle_whom_cmd(self, payload):
        data = payload['data']
        text = data['text']
        user = data['user']

        mentions = [i for i in text.split(' ') if i.startswith('<@') and i.endswith('>')]

        if not self.msg_payload and len(mentions) > 0:
            self.msg_payload = payload
            self.msg_user_id = user
            self.guess_user_id = self.get_user_id(mentions[0])
            print(f'guess received: text={text}, guesser={user}, guessed-user={self.guess_user_id}')

            payload['web_client'].reactions_add(
                name='speech_balloon',
                channel=data['channel'],
                timestamp=data['ts'])
            Timer(5, self.reset).start() # reset after delay
        return

    def handle_bot_message(self, payload):
        data = payload['data']
        text = data['text']

        if self.msg_user_id and self.guess_user_id and text.startswith(':microphone: This track,'):
            self.actual_user_id = self.get_user_id(text)
            self.track = text.split('This track, ')[1].split(', was last requested')[0]
            print(f'bot response received:, actual={self.actual_user_id}, track={self.track}')
            self.respond()
        return

    def respond(self):
        if self.msg_payload and self.msg_user_id and self.guess_user_id and self.actual_user_id and self.track:
            success = self.guess_user_id == self.actual_user_id
            # todo: randomly choose response from a set
            if success:
                text = 'Correct!'
                reaction = 'white_check_mark'
            else:
                text = 'Better luck next time!'
                reaction = 'x'

            web_client = self.msg_payload['web_client']
            web_client.chat_postMessage(channel=os.environ['CHANNEL_ID'], text=text)
            web_client.reactions_add(
                name=reaction,
                channel=self.msg_payload['data']['channel'],
                timestamp=self.msg_payload['data']['ts'])
        self.reset()
        return

    def reset(self):
        # todo: remove all reactions if exist on self.msg_payload
        # web_client.reactions_get(channel, timestamp)
        # check response and remove all reactions!
        # https://api.slack.com/methods/reactions.get
        print('\nRESETTING\n')
        self.msg_payload = None
        self.msg_user_id = None
        self.guess_user_id = None
        self.actual_user_id = None
        self.track = None

    # eg text: '/whom <@UD51HSESC|joe>'
    def get_user_id(self, str):
        return str.split('<@')[1].split('|')[0]

