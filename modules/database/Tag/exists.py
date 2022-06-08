from . import Tag, tag_collection

def exists(name:str) -> bool:
    document = tag_collection.find_one({'name':name})
    if document == None:
        return False
    else:
        return True
