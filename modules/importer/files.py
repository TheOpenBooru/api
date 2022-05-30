from . import normalise_tags
from modules import database,posts,settings
from tqdm import tqdm
from pathlib import Path
import logging

IMPORT_DIR = Path(settings.IMPORT_LOCAL_PATH)

async def import_files():
    tag_files = {}
    data_files = {}
    for file in IMPORT_DIR.iterdir():
        if file.name == '.gitignore':
            continue
        
        if file.name.endswith('.txt'):
            tag_files[file.stem] = file
        else:
            data_files[file.stem] = file

    for name in tqdm(data_files.keys()):
        data_file = data_files[name]
        if name not in tag_files:
            tag_file = None
        else:
            tag_file = tag_files[name]
        
        try:
            await import_file(data_file,tag_file)
        except Exception as e:
            logging.debug(f"Could not import {name}")
            logging.debug(f"Reason {e}")

async def import_file(data_file:Path,tag_file:Path|None):
    if tag_file == None:
        tags = []
    else:
        with open(tag_file) as f:
            tags = f.readlines()
    tags = normalise_tags(tags)

    data = data_file.read_bytes()
    post = await posts.create(data,data_file.name)
    post.tags = tags
    database.Post.update(post.id,post)
