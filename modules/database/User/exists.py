from . import user_collection

def exists(id:int) -> bool:
    document = user_collection.find_one({'id':id})
    return bool(document)