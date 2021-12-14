from typing import Literal as _Literal, Union as _Union


def create(id:int,password:str):
    """Create a new user sign-in

    Args:
        id (int): [description]
        password (str): [description]

    Raises:
        KeyError: User ID already exists
        ValueError: Password Does Not Meet Requirements
    """

def login(id:int,password:str,data:dict) -> _Union[dict,_Literal[False]]:
    """Login and Generate a JWT

    Args:
        id (int): User's ID
        password (str): The User's Passowrd
        data (dict): The data to encode into the JWT
    
    Raises:
        LookupError: Non-Existant User ID

    Returns:
        JWT | False: JWT if successful, False if invalid
    """

def verify(token:str) -> _Union[dict,_Literal[False]]:
    """
    Returns:
        Data | False: False if Token is Valid, otherwise the Token's Data
    """

def update(id:int,old_password:str,new_password:str):
    """Updates the user's password

    Args:
        id (int): User's ID
        old_password (str): The User's old password
        new_password (str): The new password
    
    Raises:
        LookupError: Non-Existant User ID
        ValueError: A Password is Invalid
    """


def delete(id:int):
    """Deletes a user's account

    Args:
        id (int): User's ID
    """


from ._crypto import create,login,verify,changePassword as update
from ._database import delete
from . import _crypto, _database
from . import test_auth as _