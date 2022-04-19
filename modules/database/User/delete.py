from . import User,_user_store

def delete(id:int):
    if id in _user_store:
        _user_store.pop(id)