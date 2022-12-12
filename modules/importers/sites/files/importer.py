from itertools import islice
from modules import posts,settings, normalise
from modules.importers import Importer, utils, run_importer
from tqdm import tqdm
from pathlib import Path
from typing import Union
import logging


# TODO: Refactor
class FileImporter(Importer):
    enabled = settings.IMPORTER_FILES_ENABLED
    time_between_runs = settings.IMPORTER_FILES_RETRY_AFTER
    _import_dir: Path

    def __init__(self, dir: str|Path|None = None):
        if dir:
            self._import_dir = Path(dir)
        else:
            self._import_dir = Path(settings.IMPORTER_FILES_BASEPATH)

    
    async def load(self, limit: Union[int, None] = None):
        tag_files = {}
        data_files = {}
        iterable = islice(self._import_dir.iterdir(), limit)
        for file in iterable:
            if file.name == '.gitignore':
                continue
            
            if file.name.endswith('.txt'):
                tag_files[file.stem] = file
            else:
                data_files[file.stem] = file
        
        for name in tqdm(data_files.keys(), desc="Importing From Files"):
            data_file = data_files[name]
            tag_file = tag_files.get(name, None)
            
            try:
                await import_file(data_file,tag_file)
            except Exception as e:
                logging.debug(f"Could not import {name}: {e}")


async def import_file(data_file:Path, tag_file:Union[Path,None]):
    if tag_file == None:
        tags = []
    else:
        with open(tag_file) as f:
            tags = f.readlines()
        tags = normalise.normalise_tags(tags)

    data = data_file.read_bytes()
    post = await posts.create(data, data_file.name)
    posts.edit(post.id, tags=tags)
