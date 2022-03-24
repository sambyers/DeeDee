import os
from webexteamssdk import WebexTeamsAPI, Webhook


class Lab():
    def __init__(self, url) -> None:
        self.base_url = url

    def get(self) -> str:
        pass
        # return self._get(f'{self.base_url}/status')
        # Returns json, e.g. {'state': 'configured', 'data': {'misc': 'Other data from running CPOC?', 'DNAC': 'blah', 'ISE': 'blah'}} OR {'state': 'default'}

    def reset(self) -> bool:
        pass
        # json = {'state': 'default'}
        # return self.put(f'{self.base_url}/lab', json)
    
    def _get(self):
        pass

class Bot():
    def __init__(self, name: str, lab: Lab, msg: str) -> None:
        self.name = name
        self.msg = msg
        self._cmd = self._parse(msg)
        self._lab = lab
        self._supported_cmds = ['help', 'status', 'reset']

    def respond(self) -> str:
        if self._validate_cmd():
            if self._cmd == 'help':
                return self._help()
            elif self._cmd == 'status':
                return self._lab.get()
            elif self._cmd == 'reset':
                return self._lab.reset()
        else:
            return self._not_implemented()
    
    def _validate_cmd(self) -> bool:
        if self.cmd in self._supported_cmds:
            return True

    def _help(self) -> str:
        return f"Hi! I'm {self.name} bot. Supported commands: /status /reset"

    def _not_implemented(self) -> str:
        return "Sorry. I don't understand your request."
    
    def _parse(self, msg: str) -> str:
        msg_list = msg.split(' ')
        for word in msg_list:
            if '/' in word:
                cmd = word.strip('/')
        return cmd


def lambda_handler(event, context):
    # Create Webhook object with webhook message
    webhook_obj = Webhook(event['body'])
    # Collect environment vars
    webhook_id = os.environ.get('WEBEX_TEAMS_WEBHOOK_ID')
    lab_url = os.environ.get('LAB_API_BASE_URL')
    bot_name = os.environ.get("BOT_NAME")
    # Confirm we're getting a request from the correct webhook
    if webhook_obj.id == webhook_id:
        # Room and message objects
        wbxapi = WebexTeamsAPI()
        room = wbxapi.rooms.get(webhook_obj.data.roomId)
        message = wbxapi.messages.get(webhook_obj.data.id)
        # Me object
        me = wbxapi.people.me()
        # Don't respond to messages from ourselves
        if not message.personId == me.id:
            # New lab object
            lab = Lab(lab_url)
            # New bot object
            bot = Bot(bot_name, lab, message.text)
            # Ask bot to respond based on message via webhook
            bot_resp = bot.respond()
            wbxapi.messages.create(room.id, text=bot_resp)
