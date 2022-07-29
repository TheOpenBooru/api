from .base import BaseStore
from modules import settings
from pathlib import Path

class LocalStore(BaseStore):
    local = True
    store_path:Path
    def __init__(self, store_path: str = settings.STORAGE_LOCAL_PATH):
        self.store_path = Path(store_path)
        if self.store_path.exists():
            self.usable = True
        else:
            self.usable = False
            self.fail_reason = "Local storage path doesn't exist"
    
    
    def put(self, data:bytes, filename:str):
        path = self.path(filename)
        if type(data) != bytes:
            raise TypeError("Data wasn't bytes")
        if path.exists():
            raise FileExistsError("The file already exists")
        
        with open(path, "wb") as f:
            f.write(data)


    def exists(self, filename:str) -> bool:
        return Path(self.store_path,filename).exists()


    def get(self, filename:str) -> bytes:
        path = self.path(filename)
        if path.parent != self.store_path:
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
        path = self.path(filename)
        path.unlink(missing_ok=True)


    def clear(self):
        for file in self.store_path.iterdir():
            if file.name != '.gitignore':
                file.unlink()


    def path(self,filename:str) -> Path:
        return self.store_path / filename