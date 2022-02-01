from modules import settings
from pathlib import Path
from typing import Generator
import numpy as np
import cv2

def generateImageVariants(img:bytes) -> Generator[bytes,None,None]:
    """Generate downscaled versions of an image

    Args:
        img (bytes): The Image Data

    Returns:
        bytes: Full Image
        bytes: Preview Image
        bytes: Thumbnail Image
    """
    options = [
        (
            settings.get('settings.posts.full.quality'),
            settings.get('settings.posts.full.max_dimensions')
        ),
        (
            settings.get('settings.posts.preview.quality'),
            settings.get('settings.posts.preview.max_dimensions')
        ),
        (
            settings.get('settings.posts.thumbnail.quality'),
            settings.get('settings.posts.thumbnail.max_dimensions')
        ),
    ]
    for quality,dimensions in options:
        yield encode(img,quality,dimensions)

def encode(img:bytes,quality:int=100,target:tuple[int,int] = None) -> bytes:
    """Raises:
        ValueError: Invalid Image Data
        ValueError: Could not parse image
    """
    image = np.asarray(bytearray(img), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    if image == None:
        raise ValueError("Invliad Image Data")
    
    suc, buf = cv2.imencode(".webp",img, [cv2.IMWRITE_WEBP_QUALITY, quality])
    if not suc:
        raise ValueError("Could not parse image")
    
    return buf.tobytes()

def getImageData(img:bytes) -> tuple[int,int,str]:
    """Raises:
        ValueError: Invalid Image Data

    Returns:
        int: Width
        int: Height
        str: Image Format
    """
    raise NotImplementedError