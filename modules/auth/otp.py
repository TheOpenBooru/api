from modules import settings
import pyotp
import re
from . import _database

class No2FAEnabled(Exception):
    "This user does not have 2FA Authentication enabled"

def _get_secret(id:int) -> str:
    user = _database.get(id)
    if user[1] == None:
        raise No2FAEnabled
    return user[1]

def generate_secret():
    "Generates a 2FA Secret"
    return pyotp.random_base32()

def generate_url(secret:str,user:str,issuer:str) -> str:
    "Generates a URL for Authenticator Apps"
    topt = pyotp.totp.TOTP(secret)
    return topt.provisioning_uri(name=user,issuer_name=issuer)

def update(id:int,secret:str):
    """Raises:
        KeyError: User with that ID doesn't exist
        ValueError: OTP is invalid
    """
    _database.get(id)
    if not re.match('/^[A-Z0-7]{32}$/',secret):
        raise ValueError("Invalid Secret")
    _database.set_2fa(id,secret)

def verify(id:int,otp:str) -> bool:
    """Verifies a User's OTP
    
    Raises:
        KeyError: User with that ID doesn't exist
        No2FASavedError: User does not have 2FA enabled
    """
    _database.get(id)
    secret = _get_secret(id)
    totp = pyotp.TOTP(secret)
    valid_window = settings.get('settings.otp.valid_window')
    return totp.verify(otp,valid_window=valid_window)

def remove(id:int):
    """Removes the 2FA from a User
    
    Raises:
        KeyError: User does not exist
    """
    _database.set_2fa(id,None)