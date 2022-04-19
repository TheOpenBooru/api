from . import User,_user_store

def create(user:User):
    """Raises:
    - KeyError: User already exists
    - ValueError: User is invalid
    """
    if user.id in _user_store:
        raise KeyError("User already exists")
    elif user.id is None:
        raise ValueError("User already exists")
    else:
        _user_store[user.id] = user
