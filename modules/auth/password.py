from modules import settings
from zxcvbn import zxcvbn

from dataclasses import dataclass

@dataclass(frozen=True)
class PasswordRequirements:
    min_length:int
    max_length:int
    score:float

def get_password_requirements() -> PasswordRequirements:
    config = settings.PASSWORD_MIN_LENGTH
    return PasswordRequirements(
        min_length=settings.PASSWORD_MIN_LENGTH,
        max_length=settings.PASSWORD_MAX_LENGTH,
        score=settings.PASSWORD_REQUIRED_SCORE,
    )

def is_password_invalid(password:str):
    requirements = get_password_requirements()
    score = zxcvbn(password)['score']
    if len(password) < requirements.min_length:
        return True
    elif len(password) > requirements.max_length:
        return True
    elif score < requirements.score:
        return True
    else:
        return False