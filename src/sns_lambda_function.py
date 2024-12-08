import logging
import sys
from typing import Dict

from repository.user_profile_repository import UserProfileRepository

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(name)s - %(levelname)s - %(asctime)s] %(message)s')


class LambdaHandler:

    def __init__(self):
        self.logger = logging.getLogger()
        self.repository = UserProfileRepository()

    def handle_event(self, event: Dict[str, object], context):
        
        # {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:ap-southeast-2:961341547325:bertybear-smart-nursery-user-change-event-sandbox:b6c28ffd-b0fc-4482-b961-06a8da105f35', 'Sns': {'Type': 'Notification', 'MessageId': '5ef8316b-976b-5bbc-8a5e-6ea51970f613', 'TopicArn': 'arn:aws:sns:ap-southeast-2:961341547325:bertybear-smart-nursery-user-change-event-sandbox', 'Subject': None, 'Message': '{"action": "INSERT", "data": {"user_id": "090e4468-30a1-7079-4b13-3cb91591c2a5", "first_name": "Eesa", "last_name": "Jacobs", "email_address": "eesa@allaboutapps.co.za"}}', 'Timestamp': '2024-12-07T17:54:35.815Z', 'SignatureVersion': '1', 'Signature': 'sHDfMhgoIfstSk3nqjpvP0g5cf7kmqAW9HUARLo/JDV2pSq7kBHCXDthAaIbNibGXH749BT92vnFaWS25gWli6k4pL3F9SzjwfKfrWH5jEWRKseWeQ/w8CP8N2NfQJflypG8wLeERt0OioZHxm8OsR1RkFXvRrN8j7hqsPG5SlGyYNrL9LhRhshN97Tk0PjCievs0YKEKjxNWqK0zQU/fX46VE7ouSNroz/jKKrmVpw7/k+5dYi0j7ZEgEPDg7gheL2yaALSGN5LcL/1+eGqa2SrG99XXLoem+DIOrgLbojGycUYCpFsrJTTX65euPc4898//xlH5u5G4m3aRUhSZg==', 'SigningCertUrl': 'https://sns.ap-southeast-2.amazonaws.com/SimpleNotificationService-9c6465fa7f48f5cacd23014631ec1136.pem', 'UnsubscribeUrl': 'https://sns.ap-southeast-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:ap-southeast-2:961341547325:bertybear-smart-nursery-user-change-event-sandbox:b6c28ffd-b0fc-4482-b961-06a8da105f35', 'MessageAttributes': {}}}]}
        message = event['Records'][0]['Sns']['Message']
        
        # we should then check if there's an existing (example a returning user)
        # in the user's table. If found, update the existing user's details accordingly

        # existing_user = self.repository.find_by_user(first_name=first_name, last_name=last_name)

        self.repository.perform_insert(message['user_id'], message['first_name'], message['last_name'], message['email_address'])

def lambda_handler(event, context):
    try:
        LambdaHandler().handle_event(event, context)
    except Exception as exception:
        raise exception
