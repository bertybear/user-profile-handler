import jwt


def get_username_from_headers(headers):
    auth_token = get_authorization_token(headers.get("Authorization"))
    decoded_token = jwt.decode(auth_token, options={"verify_signature": False})
    return decoded_token.get("username") 

def get_authorization_token(auth_header):
    if auth_header:
        # Extract the token (assuming Bearer token format)
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        return token
    else:
        return None