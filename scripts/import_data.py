from pathlib import Path
import requests

IMPORT_PATH = Path('./data/import')

def generate():
    for file in IMPORT_PATH.iterdir():
        tags_file = IMPORT_PATH / (file.stem + '.txt')
        tags = _load_tags_from_file()
        
        yield file
    ...


def _load_tags_from_file(file:Path):
    with open(file,'r') as f:
        tags = f.read().splitlines()
    return tags

def _create_file(file:Path,tags:list[str]):
    requests.post()
    if not file.exists():
        file.touch()