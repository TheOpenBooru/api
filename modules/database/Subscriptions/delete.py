from . import Subscription, collection

def delete(id:int):
    collection.delete_one({"id": id})
