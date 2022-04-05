from modules import settings as _settings
import secrets as _secrets
import time as _time
import jwt as _jwt
from dataclasses import dataclass as _dataclass

_SECRET_KEY = _secrets.token_hex(64)

@_dataclass()
class TokenData:
    userID: int
    data: dict

class BadTokenError(Exception):
    "The Token was Invalid, could be Corrupt, Invalid, Expired"

def create(id:int, additional_data:dict = {}, expiration:int|None = None) -> str:
    """Raises:
    - ValueError: Data cannot contain the reserved field
    """
    if "exp" in additional_data:
        raise ValueError(f"Data cannot contain a rerved field: 'exp'")
    if "_user_id" in additional_data:
        raise ValueError(f"Data cannot contain a rerved field: '_user_id'")

    if  expiration == None:
        expiration = _settings.DEFAULT_TOKEN_EXPIRATION

    data = {
        "exp": _time.time() + expiration, # type: ignore
        "_user_id": id
    }
    data |= additional_data
    return _jwt.encode(data, _SECRET_KEY, algorithm="HS256")


def decode(token: str) -> TokenData:
    """Raises:
    - BadTokenError: Malformed or Invalid Token
    """
    try:
        data: dict = _jwt.decode(token, _SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise BadTokenError("Malformed or Invalid Token")
    
    user_id = data["_user_id"]
    data.pop("_user_id")
    data.pop("exp")
    return TokenData(user_id, data)
