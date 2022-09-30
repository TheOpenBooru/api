from modules import settings
from zxcvbn import zxcvbn
from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordRequirements:
    min_length:int
    max_length:int
    score:float


def getPasswordRequirements() -> PasswordRequirements:
    return PasswordRequirements(
        min_length=settings.PASSWORD_MIN_LENGTH,
        max_length=settings.PASSWORD_MAX_LENGTH,
        score=settings.PASSWORD_REQUIRED_SCORE,
    )


def isPasswordValid(password:str) -> bool:
    requirements = getPasswordRequirements()
    if password == "":
        return False
    
    score = zxcvbn(password).get("score",0)
    if len(password) < requirements.min_length:
        return False
    elif len(password) > requirements.max_length:
        return False
    elif score < requirements.score:
        return False
    else:
        return True