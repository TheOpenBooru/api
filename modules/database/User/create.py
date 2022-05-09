from . import User, user_collection

def create(user:User):
    """Raises:
    - KeyError: User already exists
    - ValueError: User is invalid
    """
    
    if user_collection.find_one({'id':user.id}):
        raise KeyError("User already exists")
    else:
        document = user.dict()
        user_collection.insert_one(document)
