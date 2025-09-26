from datetime import datetime, timedelta
import json
import logging
import sys
from typing import Dict

from repository.device_metadata_repository import DeviceMetadataRepository
from repository.user_metadata_repository import UserMetadataRepository

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(name)s - %(levelname)s - %(asctime)s] %(message)s')


class SnsEventHandler:

    def __init__(self):
        self.logger = logging.getLogger()
        self.user_repository = UserMetadataRepository()
        self.device_repository = DeviceMetadataRepository()

    def handle_event(self, event: Dict[str, object], context):
        
        message = json.loads(event['Records'][0]['Sns']['Message'])
        
        if(message.get('typeOfChange') == 'INSERT'):
            data = message.get("data")
            user_id = data.get('user_id')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email_address = data.get('email_address')

            existing_devices = self.user_repository.get_volatile_devices(email_address)

            self.user_repository.create_profile(user_id, first_name, last_name, email_address)
            self.user_repository.create_cognito_username_map(email_address, user_id)
            self.user_repository.create_push_tokens_map(user_id)
            self.user_repository.create_devices_map(user_id, existing_devices)
            
            if existing_devices and len(existing_devices) > 0:
                device_ids = [device.get("device_id") for device in existing_devices]
                users = [user for user in self.device_repository.batch_get_users(device_ids)]
                for index, user in enumerate(users):
                    if user.get("user_id") == email_address:
                        user["user_id"] = user_id
                        user["status"] = self._is_device_user_invitation_expired(user) and "invite_expired" or "active"
                        self.device_repository.update_user(user.get("device_id"), index, user)
                        
            self.user_repository.delete_volatile_devices(email_address)
            self.user_repository.delete_volatile_profile(email_address)
            


    def _is_device_user_invitation_expired(self, user) -> bool:
        created_at = datetime.fromisoformat(user.get("created_at"))
        expires_at = created_at + timedelta(days=5)

        return expires_at < datetime.now()

def sns_event_handler(event, context):
    try:
        SnsEventHandler().handle_event(event, context)
        return None
    except Exception as exception:
        raise exception