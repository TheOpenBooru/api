from openbooru.modules import schemas, database, account

class InvalidUsername(Exception): pass
class InvalidPassword(Exception): pass
class UsernameAlreadyExists(Exception): pass


def create(username:str,password:str):
    """Raises:
        - InvalidUsername
        - InvalidPassword
        - AccountAlreadyExists
    """
    _validate(username, password)
    _insert(username, password)


def _validate(username:str, password:str):
    if database.User.existsByUsername(username):
        raise UsernameAlreadyExists
    
    if not account.isPasswordValid(password):
        raise InvalidPassword


def _insert(username:str, password:str):
    user = schemas.User(
        id=database.User.get_unique_id(),
        username=username,
    )

    account.register(username,password)
    database.User.insert(user)