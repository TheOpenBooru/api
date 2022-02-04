from modules import settings
import time as _time
import jwt as _jwt
from cryptography.hazmat.backends import default_backend as _default_backend
from cryptography.hazmat.primitives.asymmetric import rsa as _rsa
from dataclasses import dataclass as _dataclass

_PRIVATE_KEY = _rsa.generate_private_key(
    public_exponent=65537, key_size=4096, backend=_default_backend()
)
_PUBLIC_KEY = _PRIVATE_KEY.public_key()

@_dataclass()
class TokenData:
    userID: int
    level:str
    data: dict

class BadTokenError(Exception):
    "The Token was Invalid, could be Corrupt, Invalid, Expired"


def create(id:int, level:str, data:dict = {}, expiration:int = None) -> str:
    """Raises:
    - ValueError: Data cannot contain the reserved field
    """
    if "exp" in data:
        raise ValueError(f"Data cannot contain a rerved field: 'exp'")
    if "_level" in data:
        raise ValueError(f"Data cannot contain a rerved field: '_level'")
    if "_user_id" in data:
        raise ValueError(f"Data cannot contain a rerved field: '_user_id'")

    if expiration == None:
        expiration = settings.get("settings.jwt.expiration")

    data = dict(data) # Prevent data mutation applying outside function
    data |= {
        "exp": _time.time() + expiration,
        "_user_id": id,
        "_level": level,
    }
    return _jwt.encode(data, _PRIVATE_KEY, algorithm="RS256")


def decode(token: str) -> TokenData:
    """Raises:
    - BadTokenError: Malformed or Invalid Token
    """
    try:
        data: dict = _jwt.decode(token, _PUBLIC_KEY, algorithms=["RS256"])
    except Exception:
        raise BadTokenError("Malformed or Invalid Token")
    else:
        user_id = data["_user_id"]
        level = data["_level"]
        data.pop("_user_id")
        data.pop("_level")
        data.pop("exp")
        return TokenData(user_id,level, data)
