from dataclasses import dataclass
from . import UserPermissions

@dataclass(frozen=True)
class Account:
    id:int
    username:str
    permissions:UserPermissions

class LoginFailure(Exception):
    pass

class InvalidToken(Exception):
    pass

class InvalidPassword(Exception):
    pass

class PasswordWasReset(Exception):
    pass

class AccountDoesntExists(Exception):
    pass

class AccountAlreadyExists(Exception):
    pass