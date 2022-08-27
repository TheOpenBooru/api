from dataclasses import replace
from . import tag_collection, exists
from typing import Union
from modules import settings, schemas

def update(tag:str,new_version:schemas.Tag):
    """Raises
    - KeyError: Tag doesn't exist
    - ValueError: Invalid Tag Namespace
    """
    if not exists(tag):
        raise KeyError("Tag doesn't exist")

    if new_version.namespace not in settings.TAGS_NAMESPACES:
        raise ValueError("Invalid Tag Namespace")

    doc = new_version.dict()
    tag_collection.replace_one(
        filter={"name": tag},
        replacement=doc,
    )
