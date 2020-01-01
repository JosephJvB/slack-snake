import os
from datetime import datetime
from PyBambooHR.PyBambooHR import PyBambooHR
from base_bot import Base_Bot

class Bamboo_Bot(Base_Bot):
    def __init__(self):
        key = os.getenv('BAMBOO_KEY')
        org = os.getenv('BAMBOO_ORG')
        self.client = PyBambooHR(api_key=key, subdomain=org)

    def handle_timeoff_cmd(self, payload):
        self.msg_payload = payload
        u_id = payload['data']['user']
        slack_data = self.get_user_by_id(u_id)
        slack_email = slack_data['user']['profile']['email']
        bamboo_data = self.client.get_employee_directory()
        email_match = [u for u in bamboo_data if u['workEmail'] == slack_email]
        if len(email_match) == 1:
            self.add_react('white_check_mark')
            bamboo_user = email_match[0]
            self.request_sickleave_today(bamboo_user)
        elif len(email_match) == 0:
            self.add_react('x')
            self.post_msg(f'No bamboo account found with slack email {slack_email}')
        else:
            self.add_react('question')
            self.post_msg(f'Found more than one bamboo account with slack email {slack_email}')
        return

    def request_sickleave_today(self, bamboo_user):
        amount = '8' if datetime.now().hour < 12 else '4'
        today = datetime.today().strftime('%Y-%m-%d')
        sick_id = os.getenv('SICKLEAVE_ID')
        data = {
            'employee_id': bamboo_user['id'],
            'start': today,
            'end': today,
            'timeOffTypeId': sick_id,
            'amount': amount,
            'dates': [{ 'ymd': today, 'amount': amount }],
            'notes': [{ 'text': 'Slack sickleave bot message' }]
        }
        try:
            r = self.client.create_time_off_request(data)
            self.post_msg(f'Bamboo time off request made for {amount}hrs sickleave, today')
            print('Made sickleave request for user', bamboo_user['displayName'])
            print(r)
            print('')
            return
        except Exception as e:
            print(e)
            self.remove_react('white_check_mark')
            self.add_react('x')
            self.post_msg(f'Whoop, ting broke fam\n{e.args}')

