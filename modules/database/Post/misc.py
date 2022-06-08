from . import Post, exists, post_collection
import random


def all() -> list[Post]:
    return list(post_collection.find())

def count() -> int:
    return post_collection.count_documents({})

def get_unused_id() -> int:
    return count() + 1

def clear():
    post_collection.delete_many({})
