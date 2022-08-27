from . import tag_collection, exists
from typing import Union
from modules import settings

def update(
        tag:str,
        namespace:Union[str, None]=None
    ):
    """Raises
    - KeyError: Tag doesn't exist
    - ValueError: Invalid Tag Namespace
    """
    if not exists(tag):
        raise KeyError("Tag doesn't exist")

    if namespace and namespace not in settings.TAGS_NAMESPACES:
        raise ValueError("Invalid Tag Namespace")
    
    if namespace:
        tag_collection.update_one(
            filter={"name": tag},
            update={"namespace": namespace}
        )
