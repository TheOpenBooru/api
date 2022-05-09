from . import post_collection

def delete(id:int):
    post_collection.delete_one({'id':id})
