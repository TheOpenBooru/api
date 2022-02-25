from modules import settings as _settings
import secrets as _secrets
import time as _time
import jwt as _jwt
from dataclasses import dataclass as _dataclass

_SECRET_KEY = _secrets.token_hex(64)

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

    if  expiration == None:
        expiration = _settings.get("settings.jwt.expiration")

    data = data.copy() # Prevent mutating data outside function
    data |= {
        "exp": _time.time() + expiration, # type: ignore
        "_user_id": id,
        "_level": level,
    }
    return _jwt.encode(data, _SECRET_KEY, algorithm="HS256")


def decode(token: str) -> TokenData:
    """Raises:
    - BadTokenError: Malformed or Invalid Token
    """
    try:
        data: dict = _jwt.decode(token, _SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise BadTokenError("Malformed or Invalid Token")
    else:
        user_id = data["_user_id"]
        level = data["_level"]
        data.pop("_user_id")
        data.pop("_level")
        data.pop("exp")
        return TokenData(user_id,level, data)
