import os
from pathlib import Path
DIR = Path('./data')

def put(data:bytes, name:str) -> bool:
    try:
        with open(Path(DIR,name),'wb') as f:
            f.write(data)
    except Exception:
        return False
    else:
        return True

def get(name:str) -> bytes:
    file = Path(DIR,name)
    if file.exists():
        with open(Path(DIR,name),'rb') as f:
            data = f.read()
        return data
    else:
        raise FileNotFoundError("Attempted to Get Non-Existant File")

def delete(name:str):
    os.remove(Path(DIR,name))