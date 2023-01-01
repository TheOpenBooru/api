from . import Subscription, collection, parse_docs
from openbooru.modules import schemas
from typing import Union


def search(index: int = 0, limit: int = 0, creator: int|None = None) -> list[Subscription]:
    filter = {}
    if creator:
        filter["creator"] = creator

    cursor = collection.find(
        filter,
        skip=index,
        limit=limit,
    )
    return parse_docs(cursor)
