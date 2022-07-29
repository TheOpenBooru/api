from . import Post, exists, post_collection
from typing import Union
from pymongo.cursor import Cursor
from modules.schemas import Post
import random


def all() -> list[Post]:
    docs = post_collection.find()
    posts = [parse_doc(doc) for doc in docs]
    return posts

def count() -> int:
    return post_collection.count_documents({})

def get_new_id() -> int:
    id = random.randint(0,2**32)
    while post_collection.find_one({'id':id}): # Keep generating IDs until it doesn't eixst
        id = random.randint(0,2**32)
    return id

def clear():
    post_collection.delete_many({})

def parse_doc(doc:dict) -> Post:
    return Post.parse_obj(doc)

def parse_docs(docs:Union[list[dict], Cursor]) -> list[Post]:
    posts = []
    for doc in docs:
        try:
            post = Post.parse_obj(doc)
        except Exception:
            pass
        else:
            posts.append(post)
    return posts
