from . import tag_collection

def clear():
    tag_collection.delete_many({})
