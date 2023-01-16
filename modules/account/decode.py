from . import Account, InvalidToken, Permissions
from modules import jwt

def decode(token: str) -> Account:
    """Raises:
    - InvalidToken: Invalid Token
    """
    try:
        account = _generate_account(token)
    except Exception:
        raise InvalidToken
    else:
        return account


def _generate_account(token:str) -> Account:
    data = jwt.decode(token)
    id, username, level = data["id"], data["username"], data["level"]
    perms = Permissions.from_level(level)
    account = Account(id, username, perms)
    return account
