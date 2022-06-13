from . import auth,PasswordWasReset,LoginFailure,AccountDoesntExists
from modules import database,jwt,schemas

def login(username:str,password:str) -> str:
    """Raises:
    - LoginFailure
    - PasswordWasReset
    - AccountDoesntExists
    """
    _validate_username(username)
    
    user = database.User.getByUsername(username)
    if auth.login(username,password):
        return _generate_token(user)
    else:
        raise LoginFailure


def _validate_username(username:str):
    try:
        user = database.User.getByUsername(username)
    except KeyError:
        raise AccountDoesntExists
    
    if not auth.exists(username):
        raise PasswordWasReset


def _generate_token(user:schemas.User) -> str:
    data = {
        "id": user.id,
        "username": user.username,
        "level": user.level
    }
    token = jwt.create(data)
    return token
