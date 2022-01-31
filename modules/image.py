from pathlib import Path

def generateImageVariants(img:bytes) -> tuple[bytes,bytes,bytes]:
    """Generate downscaled versions of an image

    Args:
        img (bytes): The Image Data

    Returns:
        bytes: Full Image
        bytes: Preview Image
        bytes: Thumbnail Image
    """
    raise NotImplementedError

def encode(img:bytes,target:tuple[int,int] = None) -> bytes:
    """Downscales an image to the target dimensions,

    Raises:
        ValueError: Invalid Image Data
    """
    raise NotImplementedError

def getImageData(img:bytes) -> tuple[int,int,str]:
    """Raises:
        ValueError: Invalid Image Data

    Returns:
        int: Width
        int: Height
        str: Image Format
    """
    raise NotImplementedError