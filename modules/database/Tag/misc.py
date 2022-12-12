from . import Tag
from typing import Union, Any
from pymongo.cursor import Cursor
from modules.schemas import Post


def parse_doc(doc: dict[str, Any]) -> Tag:
    return Tag.parse_obj(doc)


def parse_docs(docs:Union[list[dict], Cursor]) -> list[Tag]:
    tags = []
    for doc in docs:
        try:
            post = Tag.parse_obj(doc)
        except Exception:
            pass
        else:
            tags.append(post)
    return tags
