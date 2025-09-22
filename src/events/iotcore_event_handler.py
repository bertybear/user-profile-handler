import logging
import sys
from typing import Dict

from repository.user_metadata_repository import UserMetadataRepository

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(name)s - %(levelname)s - %(asctime)s] %(message)s')


class IotCoreEventHandler:

    def __init__(self):
        self.logger = logging.getLogger()
        self.repository = UserMetadataRepository()

    def handle_event(self, event: Dict[str, object], context):
        device_id = event['device_id']
        principal_id = event['principal_id']

        self.repository.save_device_mapping(principal_id, device_id)

def iotcore_event_handler(event, context):
    try:
        IotCoreEventHandler().handle_event(event, context)
        return None
    except Exception as exception:
        raise exception