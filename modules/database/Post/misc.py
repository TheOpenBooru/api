from . import Post, exists, post_collection
import random


def all() -> list[Post]:
    return list(post_collection.find())

def count() -> int:
    return post_collection.count_documents({})

def get_unused_id() -> int:
    new_id = random.randint(1,2**31)
    while exists(new_id):
        new_id = random.randint(1,2**31)
    return new_id

def clear():
    post_collection.delete_many({})
