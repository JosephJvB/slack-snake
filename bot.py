import os
import random
from threading import Timer
from db import Records
from peewee import fn

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
        self.locked = False

    def handle_whom_cmd(self, payload):
        data = payload['data']
        text = data['text']
        user = data['user']

        msg_args = text.split(' ')

        if not self.msg_payload and len(msg_args) > 0:
            self.msg_payload = payload
            self.msg_user_id = user
            self.guess_user_id = msg_args[0]
            print(f'guess received: text={text}, guesser={user}, guessed-user={self.guess_user_id}')

            payload['web_client'].reactions_add(
                name='speech_balloon',
                channel=data['channel'],
                timestamp=data['ts'])
            Timer(5, self.reset).start()
        return

    def handle_bot_message(self, payload):
        self.locked = True
        data = payload['data']
        text = data['text']

        if self.msg_user_id and self.guess_user_id and text.startswith(':microphone: This track,'):
            self.actual_user_id = text.split('was last requested by ')[1]
            self.track = text.split('This track, ')[1].split(', was last requested')[0]
            print(f'bot response received:, actual={self.actual_user_id}, track={self.track}')
            self.respond()
        self.locked = False
        self.reset()
        return

    def respond(self):
        if self.msg_payload and self.msg_user_id and self.guess_user_id and self.actual_user_id and self.track:
            success = self.guess_user_id == self.actual_user_id
            web_client = self.msg_payload['web_client']
            web_client.chat_postMessage(
                channel=os.environ['CHANNEL_ID'],
                text=self.get_response_text(success))
            web_client.reactions_add(
                name= 'white_check_mark' if success else 'x',
                channel=self.msg_payload['data']['channel'],
                timestamp=self.msg_payload['data']['ts'])
            if success:
                Records.create(user=self.msg_user_id, track=self.track)
        return

    def reset(self):
        if self.locked: return
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

    def get_response_text(self, success):
        win_msgs = ['Great job!', 'Correct!', 'Mind reader!', 'Muy epico!', 'Tres bien, mon ami!']
        lose_msgs = ['Better luck next time', 'No way!', 'Not even close!', 'That\'s a no from me', 'Negative on that one']
        l = win_msgs if success else lose_msgs
        return random.choice(l)

    def handle_leaderboard_cmd(self, payload):
        web_client = payload['web_client']
        web_client.reactions_add(
            name='speech_balloon',
            channel=payload['data']['channel'],
            timestamp=payload['data']['ts'])
        query_results = (Records.select(Records.user, fn.COUNT('*')
            .alias('count'))
            .group_by(Records.user))
        if len(query_results) == 0:
            text = 'Nobody has any points yet!'
        else:
            text = '*Leaderboard:*\n'
            for r in query_results[:3]:
                text += f'<@{r.user}>: *{r.count}*\n'
        web_client.chat_postMessage(
            channel=payload['data']['channel'],
            text=text)
        return