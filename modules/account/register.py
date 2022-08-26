from . import AccountAlreadyExists,InvalidPassword,Account,auth,isPasswordValid
from modules import database,schemas

def register(username:str,password:str):
    """Raises:
    - AccountAlreadyExists
    - InvalidPassword
    """
    _validate_user(username,password)
    _create_account(username,password)


def _validate_user(username:str,password:str):
    try:
        database.User.getByUsername(username)
    except KeyError:
        pass
    else:
        raise AccountAlreadyExists

    if not isPasswordValid(password):
        raise InvalidPassword


def _create_account(username:str,password:str):
    user = schemas.User(
        id=database.User.get_unique_id(),
        username=username,
    )
    auth.register(username,password)
    database.User.insert(user)
