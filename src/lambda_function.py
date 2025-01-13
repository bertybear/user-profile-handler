import json
import os

# from aws_lambda_powertools import Logger
from config.amazon_factory import AmazonSqsFactory
from events.apigateway_event_handler import apigateway_event_handler
from events.sns_event_handler import sns_event_handler

def lambda_handler(event, context):
    try:
        if 'routeKey' in event:
            return apigateway_event_handler(event, context)
        elif 'Records' in event:
            return sns_event_handler(event, context)
    except Exception as exception:
        dead_letter_queue = AmazonSqsFactory().Queue(os.getenv('DEAD_LETTER_QUEUE_URL'))
        dead_letter_queue.send_message(MessageBody=json.dumps(event))
        
        # Logger().exception(exception)
    
        raise exception
