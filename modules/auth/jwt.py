from . import _database
import jwt as _jwt
import os
import time
import json

_SECRET = os.environ.get('JWT_SECRET',default='pepper')

class BadTokenError(Exception):
    "The Token was Invalid, could be Corrupt, Invalid, Expired"

def create(id:int,data:dict={},expiration:int=6604800) -> str:
    """Create a JWT

    Raises:
        TypeError: Data cannot be saved as JSON
    """
    try:
        json.dumps(data)
    except Exception:
        raise TypeError("Data cannot be saved as JSON")
    
    data |= {'user_id':id}
    data |= {'exp':time.time() + expiration}
    return _jwt.encode(
        data,
        _SECRET,
        algorithm="HS256"
    )

def decode(token:str) -> dict:
    """Validate and Get Data from a JWT
    
    Raises:
        BadTokenError: Malformed or Invalid Token
    
    Returns:
        dict: The Data from the Token with a user_id key
    """
    try:
        header = _jwt.get_unverified_header(token)
        data = _jwt.decode(
            token,
            key=os.getenv('JWT_SECRET'),
            algorithms=[header['alg']]
        )
    except Exception:
        raise BadTokenError("Malformed or Invalid Token")
    
    return data
