from .hash import hash,compare
from .password import is_password_invalid

Users = {}

def login(user_id:str,password:str):
    return (
        user_id in Users and
        compare(password,Users[user_id])
    )

def register(user_id:str,password:str):
    """Raises:
    - KeyError: User already exists
    - ValueError: Password is invalid
    """
    if user_id in Users:
        raise KeyError('User already exists')
    elif is_password_invalid(password):
        raise ValueError('Password is invalid')
    else:
        Users[user_id] = hash(password)

def change_password(user_id:str,password:str):
    """Raises:
    - KeyError: User does not exist
    - ValueError: Password is not valid"""
    if user_id not in Users:
        raise KeyError(f'User does not exist')
    elif is_password_invalid(password):
        raise ValueError(f"Password is invalid")
    else:
        Users[user_id] = hash(password)

def delete(user_id:str):
    Users.pop(user_id,None)
