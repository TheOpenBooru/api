from . import User,user_collection

def delete(id:int):
    user_collection.delete_one({'id':id})
