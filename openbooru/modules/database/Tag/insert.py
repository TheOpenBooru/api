from . import Tag, tag_collection, exists
from openbooru.modules.schemas import Tag


def insert(tag:Tag):
    """Raises
    - KeyError: Tag already exist
    """
    if exists(tag.name):
        raise KeyError("Tag already exist")
    else:
        document = tag.dict()
        tag_collection.insert_one(document)
