import configparser
import json
import os
import boto3
import jwt

from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools import Logger

from config.amazon_factory import AmazonSqsFactory
from config.jwt_utils import get_username_from_headers
from config.placeholder_utils import replace_placeholders
from repository.user_profile_repository import UserProfileRepository

logger = Logger()
app = APIGatewayHttpResolver()
sns_client = boto3.client('sns')

repository = UserProfileRepository()

config = configparser.ConfigParser()
config.read('app.config')

@app.get("/api/v1/user-profile")
def get_user_profile():

    username = get_username_from_headers(app.current_event.headers)
        
    user_profile = repository.find_by_username(username)
    if user_profile is None:
        return {}, 404
            
    del user_profile['username']
    return user_profile

@app.delete("/api/v1/user-profile")
def get_user_profile():

    username = get_username_from_headers(app.current_event.headers)
        
    user_profile = repository.find_by_username(username)
    if user_profile is None:
        return {}, 404
    
    repository.perform_delete(user_profile.get("email_address"))
    
    publish_sns_message('iot-device-member-change.sns.topic.arn', {
        "typeOfChange": "DELETE",
        "data": {
            "username": user_profile["username"]
        }
    })
        
    
def publish_sns_message(topic_config_key, message):
    topic_arn = config.get('DEFAULT', topic_config_key)
    topic_arn = replace_placeholders(topic_arn)
    
    sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message)
    )


def apigateway_event_handler(event: dict, context: LambdaContext) -> dict:
    try:
        return app.resolve(event, context)
    except Exception as exception:
        dead_letter_queue = AmazonSqsFactory().Queue(os.getenv('DEAD_LETTER_QUEUE_URL'))
        dead_letter_queue.send_message(MessageBody=json.dumps(event))
    
        raise exception