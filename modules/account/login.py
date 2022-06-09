from . import auth,PasswordWasReset,LoginFailure
from modules import database,jwt,schemas

def login(username:str,password:str) -> str:
    """Raises:
    - LoginFailure
    - PasswordWasReset
    """
    _validate_username(username)
    
    user = database.User.getByUsername(username)
    
    if not auth.login(username,password):
        raise LoginFailure
    else:
        return _generate_token(user)


def _validate_username(username:str):
    if not auth.exists(username):
        raise PasswordWasReset
    
    try:
        database.User.getByUsername(username)
    except KeyError:
        raise LoginFailure


def _generate_token(user:schemas.User) -> str:
    data = {
        "id": user.id,
        "username": user.username,
        "level": user.level
    }
    token = jwt.create(data)
    return token
