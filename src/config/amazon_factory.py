import boto3


class AmazonCongnitoIdpFactory:

    def __new__(cls, endpoint: str = None, region: str = None):
        if endpoint is None or region is None:
            return boto3.client('cognito-idp')

        return boto3.client('cognito-idp',
                              endpoint_url=endpoint,
                              region_name=region)

class AmazonDynamoDbFactory:

    def __new__(cls, endpoint: str = None, region: str = None):
        if endpoint is None or region is None:
            return boto3.resource('dynamodb')

        return boto3.resource('dynamodb',
                              endpoint_url=endpoint,
                              region_name=region)

class AmazonSqsFactory:

    def __new__(cls, endpoint: str = None, region: str = None):
        if endpoint is None or region is None:
            return boto3.resource('sqs')

        return boto3.resource('sqs',
                              endpoint_url=endpoint,
                              region_name=region)