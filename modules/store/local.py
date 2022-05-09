from modules import settings
import hashlib
from pathlib import Path

STORE_PATH = Path(settings.STORAGE_LOCAL_PATH)

def put(data: bytes,suffix:str = "") -> str:
    """Raises:
        TypeError: Data wasn't bytes

    Returns:
        Key: ID for the data store
    """
    if type(data) != bytes:
        raise TypeError("Data wasn't bytes")
    key = hashlib.sha256(data).hexdigest()
    key += suffix
    path = STORE_PATH / key
    with open(path, "wb") as f:
        f.write(data)
    return key


def get(key: str) -> bytes:
    """Raises:
    FileNotFoundError: Path Traversal Detected
    FileNotFoundError: Key doesn't exist
    """
    path = STORE_PATH / key
    if STORE_PATH != path.parent:
        raise FileNotFoundError("Path Traversal Detected")
    if not path.exists():
        raise FileNotFoundError("Key doesn't exist")
    with open(path, "rb") as f:
        return f.read()


def url(key: str) -> str:
    hostname = settings.HOSTNAME
    port = settings.PORT
    if port == 80:
        return f"http://{hostname}/image/{key}"
    elif port == 443:
        return f"https://{hostname}/image/{key}"
    else:
        if settings.SSL_ENABLED:
            return f"https://{hostname}:{port}/image/{key}"
        else:
            return f"http://{hostname}:{port}/image/{key}"


def delete(key: str):
    path = STORE_PATH / key
    path.unlink(missing_ok=True)


def clear():
    for file in STORE_PATH.iterdir():
        if file.name != '.gitignore':
            file.unlink()