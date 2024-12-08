import jwt

from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext
from aws_lambda_powertools import Logger

from repository.user_profile_repository import UserProfileRepository

logger = Logger()
app = APIGatewayHttpResolver()

repository = UserProfileRepository()

@app.get("/api/v1/user-profile")
def get_user_profile():
    auth_token = get_authorization_token()

    try:
        decoded_token = jwt.decode(auth_token, options={"verify_signature": False})
        username = decoded_token.get("username")

        user_profile = repository.find_by_username(username)
        del user_profile['username']

        return user_profile
    except Exception as e:
        logger.error(f"Error retrieving identity pool ID: {str(e)}")
        return {"statusCode": 500, "body": "Internal Server Error"}

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