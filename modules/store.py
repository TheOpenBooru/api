import os
from pathlib import Path


def put(key:str,data:bytes):
    """Raises:
        FileExistsError: A file with that key already exists
    """
    path = Path(f"./data/files/{key}")
    if path.exists():
        raise FileExistsError("Key already exists")
    with open(path,'wb') as f:
        f.write(data)


def get(key:str) -> bytes:
    """Raises:
        FileNotFoundError: Key does not exist
    """
    path = Path(f"./data/files/{key}")
    if not path.exists():
        raise FileNotFoundError("Key doesn't exist")
    with open(path,'rb') as f:
        return f.read()


def url(key:str) -> str:
    get(key)
    return f"http://{os.getenv('HOSTNAME')}:{os.getenv('PORT')}/files/{key}"


def delete(key:str):
    path = Path(f"./data/files/{key}")
    path.unlink(missing_ok=True)
