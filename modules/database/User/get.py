from . import User,_user_store

def get(id:int):
    """Raises:
    KeyError: User does not exist
    """
    if id not in _user_store:
        raise KeyError("User does not exist")
    return _user_store[id]
