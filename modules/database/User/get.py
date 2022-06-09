from . import User,user_collection

def get(id:int) -> User:
    """Raises:
    KeyError: User does not exist
    """
    document = user_collection.find_one({'id':id})
    if document == None:
        raise KeyError("User does not exist")
    else:
        user = User.parse_obj(document)
        return user

def getByUsername(username:str) -> User:
    """Raises:
    KeyError: User does not exist
    """
    document = user_collection.find_one({'username':username})
    if document == None:
        raise KeyError("User does not exist")
    else:
        user = User.parse_obj(document)
        return user
