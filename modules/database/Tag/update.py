from dataclasses import replace
from . import tag_collection, exists
from modules import schemas

def update(tag:str, new_version:schemas.Tag):
    """Raises
    - KeyError: Tag doesn't exist
    """
    
    doc = new_version.dict()
    res = tag_collection.find_one_and_replace(
        filter={"name": tag},
        replacement=doc,
        return_document=True,
    )
    if res == None:
        raise KeyError("Tag not found")