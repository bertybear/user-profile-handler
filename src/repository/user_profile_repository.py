import configparser
import datetime

from boto3.dynamodb.conditions import Key
from config.amazon_factory import AmazonDynamoDbFactory
from config.placeholder_utils import replace_placeholders


class UserProfileRepository:

    def __init__(self):
        self.dynamodb = AmazonDynamoDbFactory()
        self.config = configparser.ConfigParser()
        self.config.read('app.config')
        
        self.dynamodb_table_name = self.config.get('DEFAULT', 'user-profiles.dynamodb.table.name')
        self.dynamodb_table_name = replace_placeholders(self.dynamodb_table_name)
        self.dynamodb_table = self.dynamodb.Table(self.dynamodb_table_name)
        
    def perform_insert(self,
                       email_address: str,
                       username: str,
                       first_name: str,
                       last_name: str,
                       created_at: str = None):
        self.dynamodb_table.put_item(
                Item={
                    "email_address": email_address.lower(),
                    "username": username,
                    "first_name": first_name.title(),
                    "last_name": last_name.title(),
                    "created_at": created_at or datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat()
                }
            )

    def find_by_username(self, username: str):
        
        index_name = self.config.get('DEFAULT', 'user-profiles.dynamodb.table.index.username')
        index_name = replace_placeholders(index_name)
        
        result = self.dynamodb_table.query(
                    IndexName=index_name,
                    KeyConditionExpression=Key('username').eq(username)
                )
        if len(result["Items"]) == 1:
            return result["Items"][0]
        
        return None
        
    # def perform_delete(self, username: str):
    #     self.table.delete_item(
    #         Key={
    #             'cognito_username': username
    #         }
    #     )