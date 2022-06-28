from . import LocalImporter, _normalise_tags
from modules import database,posts,settings
from tqdm import tqdm
from pathlib import Path
from typing import Union
import logging


class Files(LocalImporter):
    name = "Files"
    enabled = settings.IMPORT_FILES_ENABLED
    async def import_default(self):
        tag_files = {}
        data_files = {}
        IMPORT_DIR = Path(settings.IMPORT_FILES_BASEPATH)
        for file in IMPORT_DIR.iterdir():
            if file.name == '.gitignore':
                continue
            
            if file.name.endswith('.txt'):
                tag_files[file.stem] = file
            else:
                data_files[file.stem] = file

        for name in tqdm(data_files.keys(),desc="Importing From Files"):
            data_file = data_files[name]
            if name not in tag_files:
                tag_file = None
            else:
                tag_file = tag_files[name]
            
            try:
                await self._import_file(data_file,tag_file)
            except Exception as e:
                logging.debug(f"Could not import {name}")
                logging.debug(f"Reason {e}")
    
    async def _import_file(self,data_file:Path,tag_file:Union[Path,None]):
        if tag_file == None:
            tags = []
        else:
            with open(tag_file) as f:
                tags = f.readlines()
        tags = _normalise_tags(tags)

        data = data_file.read_bytes()
        await posts.create(
            data,
            data_file.name,
            additional_tags=tags
        )
