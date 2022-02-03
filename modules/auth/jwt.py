from modules import settings
import jwt as _jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import time
import json

_PRIVATE_KEY = rsa.generate_private_key(
    public_exponent=65537, key_size=4096, backend=default_backend()
)
_PUBLIC_KEY = _PRIVATE_KEY.public_key()


class BadTokenError(Exception):
    "The Token was Invalid, could be Corrupt, Invalid, Expired"


def create(id: int, data: dict = {}, expiration: int = None) -> str:
    """Raises:
    ValueError: Data cannot contain the reserved field
    """
    if "exp" in data:
        raise ValueError(f"Data cannot contain a rerved field: 'exp'")
    if "_user_id" in data:
        raise ValueError(f"Data cannot contain a rerved field: '_user_id'")

    if expiration == None:
        expiration = settings.get("settings.jwt.expiration")

    data = dict(data) # Prevent data mutation applying outside function
    data |= {
        "exp": time.time() + expiration,
        "_user_id": id
    }
    return _jwt.encode(data, _PRIVATE_KEY, algorithm="RS256")


def decode(token: str) -> tuple[int, dict]:
    """Raises:
        BadTokenError: Malformed or Invalid Token

    Returns:
        int: The User's ID
        dict: The Data in the token
    """
    try:
        data: dict = _jwt.decode(token, _PUBLIC_KEY, algorithms=["RS256"])
    except Exception:
        raise BadTokenError("Malformed or Invalid Token")
    else:
        userID = data["_user_id"]
        data.pop("_user_id")
        data.pop("exp")
        return userID, data
