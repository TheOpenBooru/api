from . import User,user_collection
from modules.schemas import User_Query

def search(query:User_Query) -> list[User]:
    if query.username:
        cursor = user_collection.find({"username":query.username})
    elif query.email:
        cursor = user_collection.find({'email':query.email})
    else:
        cursor = user_collection.find({})
    
    users = [User.parse_obj(doc) for doc in cursor]
    return users