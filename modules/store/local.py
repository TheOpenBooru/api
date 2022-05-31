from .base import BaseStore
from modules import settings
from pathlib import Path

STORE_PATH = Path(settings.STORAGE_LOCAL_PATH)

class LocalStore(BaseStore):
    local = True
    def __init__(self):
        if STORE_PATH.exists():
            self.usable = True
        else:
            self.usable = False
            self.fail_reason = "Local storage path doesn't exist"
    
    
    def put(self, data:bytes, filename:str):
        path = STORE_PATH / filename
        if type(data) != bytes:
            raise TypeError("Data wasn't bytes")
        if path.exists():
            raise FileExistsError("The file already exists")
        
        with open(path, "wb") as f:
            f.write(data)


    def get(self, filename:str) -> bytes:
        path = STORE_PATH / filename
        if path.parent != STORE_PATH:
            raise FileNotFoundError("Path Traversal Detected")
        elif not path.exists():
            raise FileNotFoundError("Key doesn't exist")
        else:
            with open(path, "rb") as f:
                return f.read()


    def url(self, filename:str) -> str:
        hostname = settings.HOSTNAME
        port = settings.PORT
        if port == 80:
            return f"http://{hostname}/image/{filename}"
        elif port == 443:
            return f"https://{hostname}/image/{filename}"
        elif settings.SSL_ENABLED:
            return f"https://{hostname}:{port}/image/{filename}"
        else:
            return f"http://{hostname}:{port}/image/{filename}"


    def delete(self, filename:str):
        path = STORE_PATH / filename
        path.unlink(missing_ok=True)


    def clear(self):
        for file in STORE_PATH.iterdir():
            if file.name != '.gitignore':
                file.unlink()