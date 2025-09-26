from events.iotcore_event_handler import iotcore_event_handler
from events.sqs_event_handler import sqs_event_handler
from events.apigateway_event_handler import apigateway_event_handler
from events.sns_event_handler import sns_event_handler

def lambda_handler(event, context):

    if 'routeKey' in event:
        return apigateway_event_handler(event, context)
    elif 'Records' in event:
        source = event['Records'][0].get('eventSource') or event['Records'][0].get('EventSource')
        
        if source == 'aws:sns':
            return sns_event_handler(event, context)
        elif source == 'aws:sqs':
            return sqs_event_handler(event, context)
    elif 'eventSource' in event and event['eventSource'] == 'aws:iot':
        return iotcore_event_handler(event, context)
