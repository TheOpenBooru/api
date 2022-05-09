from .hash import hash,compare
from . import database
from .password import is_password_valid

def login(username:str,password:str):
    user = database.get(username)
    if user == None:
        return False
    else:
        hash = user.hash
        return compare(password, hash)

def register(username:str,password:str):
    """Raises:
    - KeyError: User already exists
    - ValueError: Password is invalid
    """
    if database.get(username) != None:
        raise KeyError('User already exists')
    elif not is_password_valid(password):
        raise ValueError('Password is invalid')
    else:
        user = database.User(
            username=username,
            hash=hash(password)
        )
        database.create(user)

def change_password(username:str,password:str):
    """Raises:
    - KeyError: User does not exist
    - ValueError: Password is not valid"""
    if database.get(username) == None:
        raise KeyError(f'User does not exist')
    elif not is_password_valid(password):
        raise ValueError(f"Password is invalid")
    else:
        database.update_hash(username,hash(password))

def exists(username:str):
    return database.get(username) != None

def delete(username:str):
    database.delete(username)
