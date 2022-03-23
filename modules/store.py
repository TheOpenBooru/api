from modules import settings
import hashlib
from pathlib import Path


STORE_PATH = Path("data","files")


def put(data: bytes,suffix:str = "",prefix:str = "") -> str:
    """Raises:
        TypeError: Data wasn't bytes

    Returns:
        Key: ID for the data store
    """
    if type(data) != bytes:
        raise TypeError("Data wasn't bytes")
    prefix = prefix + "_" if prefix else ""

    key = hashlib.sha3_256(data).hexdigest()
    key = prefix + key + suffix
    path = STORE_PATH / key
    with open(path, "wb") as f:
        f.write(data)
    return key


def get(key: str) -> bytes:
    """Raises:
    KeyError: Key doesn't exist
    """
    path = STORE_PATH / key
    if not path.exists():
        raise FileNotFoundError("Key doesn't exist")
    with open(path, "rb") as f:
        return f.read()


def url(key: str) -> str:
    hostname = settings.get("settings.site.hostname")
    port = settings.get("settings.site.port")
    return f"http://{hostname}:{port}/image/{key}"


def delete(key: str):
    path = STORE_PATH / key
    path.unlink(missing_ok=True)


def clear():
    for file in STORE_PATH.iterdir():
        file.unlink()