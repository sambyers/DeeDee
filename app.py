import os
import json
from webexteamssdk import WebexTeamsAPI, Webhook


class Lab():
    def __init__(self, url) -> None:
        self.base_url = url

    def get(self) -> str:
        return 'Lab info: BLAH'
        # return self._get(f'{self.base_url}/status')
        # Returns json, e.g. {'state': 'configured', 'data': {'misc': 'Other data from running CPOC?', 'DNAC': 'blah', 'ISE': 'blah'}} OR {'state': 'default'}

    def reset(self) -> dict:
        return json.dumps({ 'state': 'default' })
        # json = {'state': 'default'}
        # return self.put(f'{self.base_url}/lab', json)
    
    def _get(self):
        pass

class Bot():
    def __init__(self, name: str, lab: Lab, msg: str) -> None:
        self.name = name
        self._valid_cmds = ['help', 'status', 'reset']
        self.msg = msg
        self.lab = lab

    @property
    def msg(self) -> str:
        return self._msg

    @msg.setter
    def msg(self, msg: str):
        # Transform message into command and validate when msg is set
        self.cmd = self._to_cmd(msg)
        self._msg = msg
    
    def _to_cmd(self, msg: str) -> str:
        cmd = self._parse_cmd(msg)
        self._validate_cmd(cmd)
        return cmd

    def _validate_cmd(self, cmd: str) -> bool:
        if cmd in self._valid_cmds:
            valid_cmd = True
        else:
            valid_cmd = False
        self._valid_cmd = valid_cmd
        return valid_cmd

    def _help(self) -> str:
        return f"Hi! I'm {self.name} bot. Supported commands: /status /reset"

    def _not_implemented(self) -> str:
        return "Command not implemented."
    
    def _parse_cmd(self, msg: str) -> str:
        msg_list = msg.split(' ')
        for word in msg_list:
            if '/' in word:
                cmd = word.strip('/')
        return cmd

    def respond(self) -> str:
        # Check if command is valid
        if self._valid_cmd:
            # Respond to supported commands
            if self.cmd == 'help':
                return self._help()
            elif self.cmd == 'status':
                return self.lab.get()
            elif self.cmd == 'reset':
                return self.lab.reset()
        else:
            return self._not_implemented()


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
