from modules import settings
from zxcvbn import zxcvbn

from dataclasses import dataclass

@dataclass(frozen=True)
class PasswordRequirements:
    min_length:int
    max_length:int
    score:float

def get_password_requirements() -> PasswordRequirements:
    config = settings.get('auth.password_requirements')
    return PasswordRequirements(
        min_length=config['min_length'],
        max_length=config['max_length'],
        score=config['score'],
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