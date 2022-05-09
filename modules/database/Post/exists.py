from . import post_collection

def exists(id:int) -> bool:
    document = post_collection.find_one({'id':id})
    return document != None