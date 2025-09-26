import configparser
from datetime import datetime
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
from repository.user_metadata_repository import UserMetadataRepository

logger = Logger()
app = APIGatewayHttpResolver()
sns_client = boto3.client('sns')

repository = UserMetadataRepository()

config = configparser.ConfigParser()
config.read('app.config')

@app.get("/api/v1/user-profile")
def get_profile():

    user_id = get_username_from_headers(app.current_event.headers)

    profile = repository.get_profile(user_id)
    if profile is None:
        return {}, 404

    return profile

# @app.delete("/api/v1/user-profile")
# def delete_profile():

#     username = get_username_from_headers(app.current_event.headers)
        
#     user_profile = repository.find_by_username(username)
#     if user_profile is None:
#         return {}, 404
    
#     repository.perform_delete(user_profile.get("email_address"))
    
#     publish_sns_message('iot-device-member-change.sns.topic.arn', {
#         "typeOfChange": "DELETE",
#         "data": {
#             "username": user_profile["username"]
#         }
#     })

@app.post("/api/v1/user-profile/push-token")
def add_push_token():

    user_id = get_username_from_headers(app.current_event.headers)
    
    body = app.current_event.json_body
    if body is None or 'token' not in body:
        return {"message": "Missing token in request body"}, 400
    
    token = body['token']
    platform = body['platform']

    repository.add_push_token(user_id, token, platform)

    return {}, 204
        
    
# def publish_sns_message(topic_config_key, message):
#     topic_arn = config.get('DEFAULT', topic_config_key)
#     topic_arn = replace_placeholders(topic_arn)
    
#     sns_client.publish(
#         TopicArn=topic_arn,
#         Message=json.dumps(message)
#     )


def apigateway_event_handler(event: dict, context: LambdaContext) -> dict:
    try:
        return app.resolve(event, context)
    except Exception as exception:
        dead_letter_queue = AmazonSqsFactory().Queue(os.getenv('DEAD_LETTER_QUEUE_URL'))
        dead_letter_queue.send_message(MessageBody=json.dumps(event))
    
        raise exception