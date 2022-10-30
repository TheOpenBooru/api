from . import collection, Subscription
from pymongo.errors import DuplicateKeyError, BulkWriteError

def insert(subscription: Subscription):
    """Raises:
    - KeyError: Subscription already exists
    """
    document = subscription.dict()
    try:
        collection.insert_one(document=document)
    except DuplicateKeyError:
        raise KeyError("Subscription already exists")

def insertMany(subscriptions: list[Subscription]):
    documents = [sub.dict() for sub in subscriptions]
    try:
        collection.insert_many(
            documents=documents,
            bypass_document_validation=True,
            ordered=False,
        )
    except BulkWriteError:
        pass
