from typing import Union
from modules import settings as _settings
import secrets as _secrets
import time as _time
import jwt as _jwt
from pathlib import Path

_SECRET_PATH = Path("./data/tokensecret.key")
if not _SECRET_PATH.exists():
    _SECRET_KEY = _secrets.token_hex(64)
    _SECRET_PATH.write_text(_SECRET_KEY)
else:
    _SECRET_KEY = _SECRET_PATH.read_text()


class BadTokenError(Exception):
    "The Token was Invalid, could be Corrupt, Invalid, Expired"

def create(data:dict, expiration:Union[int, None] = _settings.DEFAULT_TOKEN_EXPIRATION) -> str:
    """Raises:
    - ValueError: Data cannot contain the reserved field
    """
    if "exp" in data:
        raise ValueError(f"Data cannot contain a rerved field: 'exp'")
    
    payload = data
    if expiration != None:
        payload = data | {"exp": _time.time() + expiration}
    return _jwt.encode(payload, _SECRET_KEY, algorithm="HS256")


def decode(token: str) -> dict:
    """Raises:
    - BadTokenError: Malformed or Invalid Token
    """
    try:
        data: dict = _jwt.decode(token, _SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise BadTokenError("Malformed or Invalid Token")
    
    if "exp" in data:
        data.pop("exp")
    
    return data
