from . import collection, Subscription
from typing import Any, Iterable
import random

def get_unique_id() -> int:
    id = random.randint(0,2**32)
    while collection.find_one({'id':id}):
        id = random.randint(0,2**32)
    return id


def clear():
    collection.delete_many({})

def parse_doc(doc:dict) -> Subscription:
    return Subscription.parse_obj(doc)


def parse_docs(docs: Iterable[dict]) -> list[Subscription]:
    posts = []
    for doc in docs:
        try:
            post = parse_doc(doc)
        except Exception:
            pass
        else:
            posts.append(post)
    return posts
