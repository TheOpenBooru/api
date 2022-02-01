from modules import settings
import jwt as _jwt
from pathlib import Path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import time
import json

_PRIVATE_KEY = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)
_PUBLIC_KEY = _PRIVATE_KEY.public_key()

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
        _PRIVATE_KEY,
        algorithm="RS256"
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
            _PUBLIC_KEY,
            algorithms=[header['RS256']]
        )
    except Exception:
        raise BadTokenError("Malformed or Invalid Token")
    return data
