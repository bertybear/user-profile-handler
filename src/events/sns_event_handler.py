import json
import logging
import sys
from typing import Dict

from repository.user_metadata_repository import UserMetadataRepository

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(name)s - %(levelname)s - %(asctime)s] %(message)s')


class SnsEventHandler:

    def __init__(self):
        self.logger = logging.getLogger()
        self.repository = UserMetadataRepository()

    def handle_event(self, event: Dict[str, object], context):
        
        message = json.loads(event['Records'][0]['Sns']['Message'])
        
        if(message.get('typeOfChange') == 'INSERT'):
            data = message.get("data")
            user_id = data.get('user_id')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email_address = data.get('email_address')
            
            self.repository.create_profile(user_id, first_name, last_name, email_address)

def sns_event_handler(event, context):
    try:
        SnsEventHandler().handle_event(event, context)
        return None
    except Exception as exception:
        raise exception