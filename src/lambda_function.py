from typing import Dict

from events.apigateway_event import apigateway_event_handler
from events.sns_event import sns_event_handler

def lambda_handler(event, context):
    if 'routeKey' in event:
        return apigateway_event_handler(event, context)
    elif 'Records' in event:
        return sns_event_handler(event, context)
