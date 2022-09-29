from typing import Union
from modules import settings, secrets
import time
import jwt


class BadTokenError(Exception):
    "The Token was Invalid, could be Corrupt, Invalid, Expired"


SECRET_KEY = secrets.get_secret("jwt")


def create(data:dict, expiration:Union[int, None] = settings.DEFAULT_TOKEN_EXPIRATION) -> str:
    """Raises:
    - ValueError: Data cannot contain the reserved field
    """
    if "exp" in data:
        raise ValueError(f"Data cannot contain a rerved field: 'exp'")
    
    payload = data
    if expiration != None:
        payload = data | {"exp": time.time() + expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode(token: str) -> dict:
    """Raises:
    - BadTokenError: Malformed or Invalid Token
    """
    try:
        data: dict = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise BadTokenError("Malformed or Invalid Token")
    
    if "exp" in data:
        data.pop("exp")
    
    return data
