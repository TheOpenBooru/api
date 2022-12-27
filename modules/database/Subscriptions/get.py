from . import Subscription, collection, parse_doc
from typing import Union

def get(id:int) -> Subscription:
    """Raises:
    KeyError: Subscription does not exist
    """
    return _get_by_filter({"id":id})


def getByUrl(url:str) -> Subscription:
    """Raises:
    KeyError: Subscription does not exist
    """
    return _get_by_filter({"url":url})


def _get_by_filter(filter:dict):
    document = collection.find_one(filter)
    if document == None:
        raise KeyError("Subscription does not exist")
    else:
        return parse_doc(document)
