from . import download_namespace_data
from modules import settings, database
from tqdm import tqdm
from typing import Union

def guess_namespace(tag:str, lookup:dict[str,str]) -> Union[str, None]:
    if tag not in lookup:
        return None
    
    namespace = lookup[tag]
    if namespace not in settings.TAGS_NAMESPACES:
        return None
    
    return namespace


def regen_namespaces():
    progress = tqdm(
        iterable=database.Tag.all(),
        desc="Regenerating Tag Namespaces",
        unit=" tag",
    )
    lookup = download_namespace_data()
    for tag in progress:
        namespace = guess_namespace(tag.name, lookup)
        if namespace:
            tag.namespace = namespace
            database.Tag.update(tag.name, tag)