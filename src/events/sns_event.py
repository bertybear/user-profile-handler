import json
import logging
import sys
from typing import Dict

from events.apigateway_event import apigateway_event_handler
from repository.user_profile_repository import UserProfileRepository

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(name)s - %(levelname)s - %(asctime)s] %(message)s')


class SnsEventHandler:

    def __init__(self):
        self.logger = logging.getLogger()
        self.repository = UserProfileRepository()

    def handle_event(self, event: Dict[str, object], context):
        
        print("Received user change event")
        
        message = json.loads(event['Records'][0]['Sns']['Message'])
        
        if(message.get('action') == 'INSERT'):
            data = message.get("data")
            email_address = data.get('email_address')
            username = data.get('username')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            # we should then check if there's an existing (example a returning user)
            # in the user's table. If found, update the existing user's details accordingly

            # existing_user = self.repository.find_by_user(first_name=first_name, last_name=last_name)
            self.repository.perform_insert(email_address, username, first_name, last_name)

def sns_event_handler(event, context):
    try:
        SnsEventHandler().handle_event(event, context)
        return None
    except Exception as exception:
        raise exception