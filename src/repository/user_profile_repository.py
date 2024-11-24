import datetime
import os

from boto3.dynamodb.conditions import Key
from config.amazon_factory import AmazonDynamoDbFactory


class UserProfileRepository:

    def __init__(self, dynamodb=None):
        self.environment_name = os.environ.get("ENV")
        self.dynamodb = dynamodb if dynamodb is not None else AmazonDynamoDbFactory()
        self.table = self.dynamodb.Table(f"{self.environment_name}-bertie-smart-nursery-user-profiles")

    def find_by_cognito_username(self, username):
        result = self.table.query(
                    KeyConditionExpression=Key('cognito_username').eq(username)
                )
        if len(result["Items"]) == 1:
            return result["Items"][0]
        
        return None
        
    def perform_delete(self, username: str):
        self.table.delete_item(
            Key={
                'cognito_username': username
            }
        )