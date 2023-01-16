from .hash import hash,compare
from . import database
from ..password import isPasswordValid

EXAMPLE_HASH = hash("")

def login(username:str,password:str) -> bool:
    user = database.get(username)
    if user == None:
        hash = EXAMPLE_HASH
    else:
        hash = user.hash
    return compare(password, hash)


def register(username:str,password:str):
    if database.get(username) != None:
        database.delete(username)
    # Above system has priority, so deleting existing users is fine
    user = database.User(
        username=username,
        hash=hash(password)
    )
    database.create(user)


def change_password(username:str,password:str):
    """Raises:
    - KeyError: User does not exist
    """
    if database.get(username) == None:
        raise KeyError(f'User does not exist')
    else:
        database.update_hash(username,hash(password))


def exists(username:str):
    return database.get(username) != None


def delete(username:str):
    database.delete(username)
