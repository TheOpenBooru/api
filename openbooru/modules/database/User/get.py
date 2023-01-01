from . import User,user_collection
from typing import Union

def get(id:int) -> User:
    """Raises:
    KeyError: User does not exist
    """
    return _get_by_filter({"id":id})


def getByUsername(username:str) -> User:
    """Raises:
    KeyError: User does not exist
    """
    return _get_by_filter({"username":username})


def getByEmail(email:str) -> User:
    """Raises:
    KeyError: User does not exist
    """
    return _get_by_filter({"email":email})


def _get_by_filter(filter:dict):
    document = user_collection.find_one(filter)
    if document == None:
        raise KeyError("User does not exist")
    else:
        user = User.parse_obj(document)
        return user
