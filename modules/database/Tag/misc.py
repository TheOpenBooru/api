from . import Tag
from typing import Union
from pymongo.cursor import Cursor
from modules.schemas import Post


def parse_doc(doc:dict) -> Tag:
    return Tag.parse_obj(doc)


def parse_docs(docs:Union[list[dict], Cursor]) -> list[Tag]:
    posts = []
    for doc in docs:
        try:
            post = Post.parse_obj(doc)
        except Exception:
            pass
        else:
            posts.append(post)
    return posts
