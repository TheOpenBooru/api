from . import _database
from passlib.hash import argon2 as _argon2
from password_strength import PasswordPolicy as _Policy

class NoPasswordSavedError(Exception):
    "The user has no password saved"

def _hashPassword(password:str) -> str:
    return _argon2.using(rounds=4).hash(password)

def _verifyPassword(password:str,hash:str) -> bool:
    return _argon2.verify(password, hash)

_policy = _Policy.from_names(strength=0.4,length=8)
def isPasswordInvalid(password:str) -> bool:
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128
    return (
        len(password) > MAX_PASSWORD_LENGTH or
        len(password) < MIN_PASSWORD_LENGTH or
        _policy.test(password) == False)

def create(id:int,password:str):
    """Create a new user sign-in

    Raises:
        KeyError: User already exists
        ValueError: Password Does Not Meet Requirements
    """
    ...
    if isPasswordInvalid(password):
        raise ValueError("Password Does Not Meet Requirements")
    hash = _hashPassword(password)
    _database.create(id,hash)

def login(id:int,password:str) -> bool:
    """Check a Login Credentials
    
    Raises:
        KeyError: User with that ID doesn't exist
        NoPasswordSavedError: The user didn't have a password saved
    """
    hash,_ = _database.get(id)
    if hash == None:
        raise NoPasswordSavedError("The user didn't have a password saved")
    return _verifyPassword(password,hash)

def delete(id:int):
    """Deletes a user's account"""
    _database.delete(id)

def change_password(id:int,password:str):
    """Updates the user's password
    
    Raises:
        KeyError: User with that ID doesn't exist
        ValueError: Password Does Not Meet Requirements
    """
    _database.get(id)
    if isPasswordInvalid(password):
        raise ValueError("Password Does Not Meet Requirements")
    hash = _hashPassword(password)
    _database.set_hash(id,hash)

def clear():
    "Clears the database of all users"
    _database.clear()