class LoginFailureError(Exception):
    """Login 
    """
    pass

class BadTokenError(Exception):
    """[summary]
    """
    pass

def create(id:int,password:str):
    """Create a new user sign-in

    Args:
        id: The ID of the user
        password: 

    Raises:
        KeyError: User ID already exists
        ValueError: Password Does Not Meet Requirements
    """
    ...

def login(id:int,password:str,*,data:dict={},expiration:int=6604800) -> str:
    """Login and Generate a JWT

    Args:
        id: User's ID
        password: The User's Passowrd
        
        data: The data to encode into the JWT
        expiration: 
    
    Raises:
        KeyError: Non-Existant User ID
        LoginFailureError: Invalid Password or Username
        TypeError: Payload is not a dict

    Returns:
        JWT: Returns the JSON Web Token
    """
    ...

def verify(token:str) -> dict:
    """Validate and Get Data from a JWT
    
    Raises:
        KeyError: User has been deleted
        BadTokenError: Invalid Token
    
    Returns:
        Data: Returns The Token's Data
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
        LoginFailureError: Old Password is Incorrect
    """
    ...


def delete(id:int):
    """Deletes a user's account

    Args:
        id (int): User's ID
    """
    ...


from ._crypto import create,login,verify,update
from ._database import delete
# from . import endpoint as _