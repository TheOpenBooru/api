from email.policy import default
from .downloader import download_tag_data
from modules import schemas, database, settings
from tqdm import tqdm
from typing import Iterable


def import_e621_tag_data():
    all_tags = database.Tag.all()
    lookup = download_tag_data(all_tags)
    progress: Iterable[schemas.Tag] = tqdm(
        iterable=all_tags,
        desc="Importing Tag Data From E621",
        unit=" tag",
    )
    for tag in progress:
        if tag.name not in lookup:
            continue
        e621_data = lookup[tag.name]
        new_tag = tag.copy()
        
        if e621_data.namespace and tag.namespace == "generic":
            if e621_data.namespace in settings.TAGS_NAMESPACES:
                new_tag.namespace = e621_data.namespace

        if e621_data.siblings and tag.siblings == []:
            new_tag.siblings = e621_data.siblings
        
        if e621_data.parents and tag.parents == []:
            new_tag.parents = e621_data.parents

        if new_tag != tag:
            database.Tag.update(tag.name, new_tag)
