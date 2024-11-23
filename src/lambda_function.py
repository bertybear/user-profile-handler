import json
import jwt

from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools import Logger

logger = Logger()
app = APIGatewayHttpResolver()

@app.get("/user-profile")
def get_user_profile():
    auth_token = get_authorization_token()

    try:
        # Decode the JWT token to get the user 'sub'
        decoded_token = jwt.decode(auth_token, options={"verify_signature": False})  # Use your public key to verify
        username = decoded_token.get("username")

        # {'sub': 'f6d2e224-6051-7084-c01c-fe5a222971d4', 'iss': 'https://cognito-idp.eu-west-2.amazonaws.com/eu-west-2_QBpffJzGv', 'client_id': '1c3jdq0r74jhlmkrsnjsgpmhgg', 'origin_jti': '83ebcc59-2c76-4665-8435-031452c8d8cc', 'event_id': 'f6c66a4f-4a61-43b2-809d-37d6aec4a8cd', 'token_use': 'access', 'scope': 'aws.cognito.signin.user.admin', 'auth_time': 1730100200, 'exp': 1730657212, 'iat': 1730655412, 'jti': '131eda4e-d5c5-446d-833c-0638598cd4a5', 'username': 'f6d2e224-6051-7084-c01c-fe5a222971d4'}

        # Get the Identity Pool ID
        identity_pool_id = ""

        return {
            "statusCode": 200,
            "body": json.dumps({"identity_pool_id": identity_pool_id}),
        }
    except Exception as e:
        logger.error(f"Error retrieving identity pool ID: {str(e)}")
        return {"statusCode": 500, "body": "Internal Server Error"}

    return {"message": "pongs"}

def get_authorization_token():
    # Get the Authorization header
    auth_header = app.current_event.headers.get("Authorization")
    if auth_header:
        # Extract the token (assuming Bearer token format)
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        return token
    else:
        logger.warning("Authorization header not found")
        return None


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)