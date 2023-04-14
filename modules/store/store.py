from modules import settings
from pathlib import Path


STORE_PATH = Path(settings.STORAGE_LOCAL_PATH)


def put(data:bytes, filename:str):
    filepath = _generate_path(filename)
    if type(data) != bytes:
        raise TypeError("Data wasn't bytes")
    if filepath.exists():
        raise FileExistsError("The file already exists")

    with open(filepath, "wb") as f:
        f.write(data)


def exists(filename: str) -> bool:
    return Path(STORE_PATH, filename).exists()


def get(filename:str) -> bytes:
    path = _generate_path(filename)
    if path.parent != STORE_PATH:
        raise FileNotFoundError("Path Traversal Detected")
    elif not path.exists():
        raise FileNotFoundError("Key doesn't exist")
    else:
        with open(path, "rb") as f:
            return f.read()


def url(filename:str) -> str:
    return f"/media/{filename}"


def delete(filename:str):
    path = _generate_path(filename)
    path.unlink(missing_ok=True)


def clear():
    for file in STORE_PATH.iterdir():
        if file.name != '.gitignore':
            file.unlink()


def _generate_path(filename: str) -> Path:
    return STORE_PATH / filename


if settings.WIPE_ON_STARTUP:
    clear()
