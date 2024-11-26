import datetime

import jwt
from django.conf import settings

# JWT settings
SECRET_KEY = settings.SECRET_KEY  # Or a custom key

ALGORITHM = "HS256"  # Using HMAC SHA-256 for JWT encoding
EXPIRATION_TIME = 3600  # Token expiration in seconds (1 hour)


def generate_jwt(user_id, username):
    """Generate JWT for the given user."""
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        seconds=EXPIRATION_TIME
    )
    payload = {"user_id": user_id, "username": username, "exp": expiration_time}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token):
    """Decode JWT and return the payload."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


def verify_jwt(token):
    """Verify the JWT and return user ID and username if valid."""
    payload = decode_jwt(token)
    if payload:
        return payload["user_id"], payload["username"]
    return None, None
