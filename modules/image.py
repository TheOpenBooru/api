from pathlib import Path

def encode(path:str | Path,target:tuple[int,int] = None) -> str | Path:
    """Downscales an image to the target dimensions,

    Raises:
        ValueError: Invalid Image Data
    """
    raise NotImplementedError