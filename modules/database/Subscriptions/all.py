from . import Subscription, collection, parse_docs
from modules import schemas
from typing import Union


def iterAll() -> list[Subscription]:
    cursor = collection.find({})
    return parse_docs(cursor)
