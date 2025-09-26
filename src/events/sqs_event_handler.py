import json
import logging
import sys
from typing import Dict

from repository.user_metadata_repository import UserMetadataRepository

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(name)s - %(levelname)s - %(asctime)s] %(message)s')


class SqsEventHandler:

    def __init__(self):
        self.logger = logging.getLogger()
        self.repository = UserMetadataRepository()

    def handle_event(self, event: Dict[str, object], context):

        event_source_arn = event['Records'][0]['eventSourceARN']
        message = json.loads(event['Records'][0]['body'])

        print(f"Received message from queue: {event_source_arn}")
        print(f"Message body: {message}")

def sqs_event_handler(event, context):
    try:
        SqsEventHandler().handle_event(event, context)
        return None
    except Exception as exception:
        raise exception