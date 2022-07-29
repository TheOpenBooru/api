from . import tag_collection

def delete(tag:str):
    tag_collection.delete_one({"name":tag})
