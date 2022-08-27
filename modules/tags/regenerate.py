from .services import get_tag_namespace
from modules import database, schemas
from tqdm import tqdm

def regenerate():
    database.Tag.regenerate()
    regen_namespaces()


def regen_namespaces():
    tags = database.Tag.all()
    progress = tqdm(
        iterable=tags,
        desc="Updating Tag Namespaces",
        unit=" tag",
    )
    
    for tag in progress:
        if tag.namespace != "generic":
            continue
        
        new_version = tag.copy()
        new_version.namespace = get_tag_namespace(tag.name)
        if tag.namespace != new_version.namespace:
            database.Tag.update(tag.name,new_version)
