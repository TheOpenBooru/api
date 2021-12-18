class AuthError(Exception):
    pass

class BadTokenError(Exception):
    pass

def create(id:int,password:str):
    """Create a new user sign-in

    Args:
        id (int): [description]
        password (str): [description]

    Raises:
        KeyError: User ID already exists
        ValueError: Password Does Not Meet Requirements
    """
    ...

def login(id:int,password:str,*,data:dict={},expiration:int=6604800) -> str:
    """Login and Generate a JWT

    Args:
        id (int): User's ID
        password (str): The User's Passowrd
        data (dict): The data to encode into the JWT
    
    Raises:
        KeyError: Non-Existant User ID
        AuthError: Invalid Password or Username
        TypeError: Payload is not a dict

    Returns:
        jwt (str): Returns the JSON Web Token
    """
    ...

def decode(token:str) -> dict:
    """
    Returns:
        Data (dict) | False: False if Token is Valid, otherwise the Token's Data

    Raises:
        KeyError: User has been deleted
        BadTokenError: Invalid Token
    """
    ...

def update(id:int,old_password:str,new_password:str):
    """Updates the user's password

    Args:
        id (int): User's ID
        old_password (str): The User's old password
        new_password (str): The new password
    
    Raises:
        KeyError: Non-Existant User ID
        ValueError: Password Does Not Meet Requirements
        AuthError: Old Password is Incorrect
    """
    ...


def delete(id:int):
    """Deletes a user's account

    Args:
        id (int): User's ID
    """
    ...


from ._crypto import create,login,decode,update
from ._database import delete
from . import endpoint as _