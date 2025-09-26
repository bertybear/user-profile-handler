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

    # Create a new user profile in the DynamoDB table
    def create_profile(self, user_id: str, first_name: str, last_name: str, email_address: str):
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
        
    # Retrieve the user profile from the DynamoDB table
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


    # Delete the volatile user profile from the DynamoDB table
    def delete_volatile_profile(self, user_id: str):
        self.dynamodb_table.delete_item(
            Key={
                "user_id": user_id,
                "entity_type": "VOLATILE_PROFILE"
            }
        )
    
    
    # Initialize an empty devices list for the user
    def create_devices_map(self, user_id: str, devices = None):
        self.dynamodb_table.put_item(
                Item={
                    "user_id": user_id,
                    "entity_type": "DEVICES",
                    "entity_value": devices or [],
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            )
    
    
    # Retrieve the list of devices associated with the user
    def get_devices(self, user_id: str):
        response = self.dynamodb_table.get_item(
            Key={
                "user_id": user_id,
                "entity_type": "DEVICES"
            }
        )
        return response.get("Item", {}).get("entity_value", [])
    
    
    # Retrieve the list of volatile devices associated with the user
    def get_volatile_devices(self, user_id: str):
        response = self.dynamodb_table.get_item(
            Key={
                "user_id": user_id,
                "entity_type": "VOLATILE_DEVICES"
            }
        )
        return response.get("Item", {}).get("entity_value", [])
    
    
    # Add a new device to the user's device list if it doesn't already exist
    def add_device(self, user_id, device_id):
        existing_devices = self.get_devices(user_id)

        # check if device already exists
        if any(device.get("device_id") == device_id for device in existing_devices):
            return

        self.dynamodb_table.update_item(
            Key={
                "user_id": user_id,
                "entity_type": "DEVICES"
            },
            UpdateExpression="SET entity_value = list_append(if_not_exists(entity_value, :empty_list), :new_device), updated_at = :updated_at",
            ExpressionAttributeValues={
                ":new_device": [{
                    "device_id": device_id,
                    "created_at": datetime.now().isoformat()
                }],
                ":empty_list": [],
                ":updated_at": datetime.now().isoformat()
            }
        )
        
    
    # Delete the volatile devices entry for the user
    def delete_volatile_devices(self, user_id: str):
        self.dynamodb_table.delete_item(
            Key={
                "user_id": user_id,
                "entity_type": "VOLATILE_DEVICES"
            }
        )
        
        
    # Initialize an empty push tokens list for the user
    def create_push_tokens_map(self, user_id: str):
        self.dynamodb_table.put_item(
                Item={
                    "user_id": user_id,
                    "entity_type": "PUSH_TOKENS",
                    "entity_value": [],
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            )
    
    
    # Retrieve the list of push tokens associated with the user
    def get_push_tokens(self, user_id: str):
        response = self.dynamodb_table.get_item(
            Key={
                "user_id": user_id,
                "entity_type": "PUSH_TOKENS"
            }
        )
        
        item = response.get("Item", {})
        return item.get("entity_value", [])


    # Add a new push token to the user's push tokens list if it doesn't already exist
    def add_push_token(self, user_id: str, push_token: str, platform: str):
        # get existing push tokens
        existing_push_tokens = self.get_push_tokens(user_id)

        # check if push token already exists
        if any(token.get("token") == push_token and token.get("platform") == platform for token in existing_push_tokens):
            return
        
        self.dynamodb_table.update_item(
            Key={
                "user_id": user_id,
                "entity_type": "PUSH_TOKENS"
            },
            UpdateExpression="SET entity_value = list_append(if_not_exists(entity_value, :empty_list), :new_token), updated_at = :updated_at",
            ExpressionAttributeValues={
                ':new_token': [{
                    "token": push_token,
                    "platform": platform,
                    "created_at": datetime.now().isoformat()
                }],
                ':empty_list': [],
                ':updated_at': datetime.now().isoformat()
            }
        )

    
    # Create a mapping from email address to Cognito username
    def create_cognito_username_map(self, email_address: str, cognito_username: str):
        self.dynamodb_table.put_item(
            Item={
                "user_id": email_address.lower(),
                "entity_type": "COGNITO_USERNAME",
                "entity_value": cognito_username,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        )