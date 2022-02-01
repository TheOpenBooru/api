from modules import settings
import jwt as _jwt
import os
import time
import json


class BadTokenError(Exception):
    "The Token was Invalid, could be Corrupt, Invalid, Expired"

def create(id:int,data:dict={},expiration:int=None) -> str:
    """Raises:
        TypeError: Data cannot be saved as JSON
    """
    try:
        json.dumps(data)
    except Exception:
        raise TypeError("Data cannot be saved as JSON")

    if expiration == None:
        expiration = settings.get('settings.jwt.expiration')
    data |= {'exp':time.time() + expiration} # type: ignore
    data |= {'user_id':id}
    return _jwt.encode(
        data,
        settings.get('config.jwt_secret'),
        algorithm="HS256"
    )

def decode(token:str) -> dict:
    """Raises:
        BadTokenError: Malformed or Invalid Token
    
    Returns:
        dict: The Data from the Token with a user_id key
    """
    try:
        header = _jwt.get_unverified_header(token)
        data = _jwt.decode(
            token,
            key=settings.get('config.jwt_secret'),
            algorithms=[header['alg']]
        )
    except Exception:
        raise BadTokenError("Malformed or Invalid Token")
    
    return data
