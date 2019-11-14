class Base_Bot(object):
    def __init__(self):
        self.msg_payload = None

    def post_msg(self, text):
        if self.msg_payload is None:
            print('post_msg: msg_payload not set!')
        else:
            self.msg_payload['web_client'].chat_postMessage(
                channel=self.msg_payload['data']['channel'],
                timestamp=self.msg_payload['data']['ts'],
                text=text)
        return

    def add_react(self, name):
        if self.msg_payload is None:
            print('add_react: msg_payload not set!')
        else:
            self.msg_payload['web_client'].reactions_add(
                name=name,
                channel=self.msg_payload['data']['channel'],
                timestamp=self.msg_payload['data']['ts'])
        return

    def remove_react(self, name):
        if self.msg_payload is None:
            print('remove_react: msg_payload not set!')
        else:
            self.msg_payload['web_client'].reactions_remove(
                name=name,
                channel=self.msg_payload['data']['channel'],
                timestamp=self.msg_payload['data']['ts'])
        return