import configparser
from datetime import datetime

from config.amazon_factory import AmazonDynamoDbFactory
from config.placeholder_utils import replace_placeholders


class UserMetadataRepository:

    def __init__(self):
        self.dynamodb = AmazonDynamoDbFactory()
        self.config = configparser.ConfigParser()
        self.config.read('app.config')
        
        self.dynamodb_table_name = self.config.get('DEFAULT', 'user-metadata.dynamodb.table.name')
        self.dynamodb_table_name = replace_placeholders(self.dynamodb_table_name)
        self.dynamodb_table = self.dynamodb.Table(self.dynamodb_table_name)
        
    def create_profile(self,
                       user_id: str,
                       first_name: str,
                       last_name: str,
                       email_address: str):
        self.dynamodb_table.put_item(
                Item={
                    "user_id": user_id,
                    "entity_type": "PROFILE",
                    "entity_value": {
                        "first_name": first_name.title(),
                        "last_name": last_name.title(),
                        "email_address": email_address.lower()
                    },
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            )
        
    def get_profile(self, user_id: str):

        result = self.dynamodb_table.get_item(
            Key={
                "user_id": user_id,
                "entity_type": "PROFILE"
            }
        )
        
        if not result.get("Item"):
            return None
        
        return result.get("Item", {}).get("entity_value", {})
    
    def get_push_tokens(self, user_id: str):
        response = self.dynamodb_table.get_item(
            Key={
                "user_id": user_id,
                "entity_type": "PUSH_TOKENS"
            }
        )
        
        return response.get("Item", {}).get("entity_value", []), response.get("Item", {}).get("created_at", None)

    def save_push_tokens(self, user_id: str, push_tokens: list, created_at: str = None):
        self.dynamodb_table.update_item(
            Key={
                "user_id": user_id,
                "entity_type": "PUSH_TOKENS"
            },
            UpdateExpression="SET entity_value = :push_tokens, updated_at = :updated_at",
            ExpressionAttributeValues={
                ':push_tokens': push_tokens,
                ':created_at': created_at or datetime.now().isoformat(),
                ':updated_at': datetime.now().isoformat()
            }
        )
        
    def save_device_mapping(self, user_id, device_id, user_role="owner", user_status="active"):
        # get existing devices
        response = self.dynamodb_table.get_item(
            Key={
                "user_id": user_id,
                "entity_type": "DEVICES"
            }
        )
        existing_devices = response.get("Item", {}).get("entity_value", [])

        # check if device already exists
        if any(device.get("device_id") == device_id for device in existing_devices):
            return
        
        created_at = response.get("Item", {}).get("created_at", datetime.now().isoformat())
        
        self.dynamodb_table.update_item(
            Key={
                "user_id": user_id,
                "entity_type": "DEVICES"
            },
            UpdateExpression="SET entity_value = list_append(if_not_exists(entity_value, :empty_list), :new_device), created_at = :created_at, updated_at = :updated_at",
            ExpressionAttributeValues={
                ":new_device": [{
                    "device_id": device_id,
                    "role": user_role,
                    "status": user_status,
                    "created_at": datetime.now().isoformat()
                }],
                ":empty_list": [],
                ":created_at": created_at,
                ":updated_at": datetime.now().isoformat()
            }
        )