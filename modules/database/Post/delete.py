from . import post_collection

def delete(id:int):
    if id > 2**63:
        return
    
    post_collection.delete_one({'id':id})
