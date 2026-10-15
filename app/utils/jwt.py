"""
JWT
"""

from datetime import datetime, timedelta, UTC
import os
import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv

load_dotenv(override=True)
jwt_secret = os.environ.get("JWT_SECRET")
algo = "HS256"


def sign_token(payload: dict) -> str:
    """签发JWT，附带过期时间"""
    new_payload = payload.copy()
    new_payload["exp"] = datetime.now(tz=UTC) + timedelta(days=1)
    return jwt.encode(new_payload, key=jwt_secret, algorithm=algo)


def verify_token(token: str) -> dict | None:
    """校验JWT，过期/无效返回None"""
    try:
        decoded_token = jwt.decode(
            token, jwt_secret, algorithms=[algo], options={"verify_exp": True}
        )
        return decoded_token
    except InvalidTokenError:
        return None
