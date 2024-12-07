import logging
import sys
from typing import Dict

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(name)s - %(levelname)s - %(asctime)s] %(message)s')


class LambdaHandler:

    def __init__(self):
        self.logger = logging.getLogger()

    def handle_event(self, event: Dict[str, object], context):
        print("Hello world")

def lambda_handler(event, context):
    try:
        LambdaHandler().handle_event(event, context)
    except Exception as exception:
        raise exception
