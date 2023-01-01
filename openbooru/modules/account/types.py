from . import Permissions
from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    id:int
    username:str
    permissions:Permissions


class LoginFailure(Exception): pass
class InvalidToken(Exception): pass
class PasswordWasReset(Exception): pass
class AccountDoesntExists(Exception): pass
