from . import Tag
from typing import Union, Any
from pymongo.cursor import Cursor
import logging


def parse_doc(doc: dict[str, Any]) -> Tag:
    return Tag.parse_obj(doc)


def parse_docs(docs:Union[list[dict], Cursor]) -> list[Tag]:
    tags = []
    for doc in docs:
        try:
            post = Tag.parse_obj(doc)
        except Exception:
            logging.warning(f"Could not parse tag in database: ID {doc.get('id', 'No ID')}")
        else:
            tags.append(post)
    return tags
