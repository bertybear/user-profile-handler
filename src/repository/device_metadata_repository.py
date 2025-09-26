import configparser
import datetime

from config.amazon_factory import AmazonDynamoDbFactory
from config.placeholder_utils import replace_placeholders


class DeviceMetadataRepository:

    def __init__(self):
        self.dynamodb = AmazonDynamoDbFactory()
        self.config = configparser.ConfigParser()
        self.config.read('app.config')
        
        self.dynamodb_table_name = self.config.get('DEFAULT', 'device.metadata.dynamodb.table.name')
        self.dynamodb_table_name = replace_placeholders(self.dynamodb_table_name)
        self.dynamodb_table = self.dynamodb.Table(self.dynamodb_table_name)
    
    
    def batch_get_users(self, device_ids):
        users = []
        keys = [{'device_id': device_id, "entity_type": "USERS"} for device_id in device_ids]

        batch_get_item_response = self.dynamodb.batch_get_item(
            RequestItems={
                self.dynamodb_table_name: {
                    'Keys': keys
                }
            }
        )

        responses = batch_get_item_response.get("Responses", [])
        
        for key in responses:
            if(key == self.dynamodb_table_name):
                users = responses[key]
                break
            
        users = [{**user, "device_id": item.get("device_id")} for item in users for user in item.get("entity_value", [])]
        return users
    
    
    def update_user(self, device_id, index, user):
        self.dynamodb_table.update_item(
            Key={
                "device_id": device_id,
                "entity_type": "USERS"
            },
            UpdateExpression=f"SET entity_value[{index}] = :user, updated_at = :updated_at",
            ExpressionAttributeValues={
                ":user": user,
                ":updated_at": datetime.datetime.now().isoformat()
            }
        )