def put(name:str,data:bytes):
    """

    Args:
        name (str): Image Name
        data (bytes): Image Data
    
    Raises:
        FileExistsError: Name Already Exists
        ValueError: Data is for an invalid image
    """

def get(name:str) -> bytes:
    """Get the image data from it's name

    Args:
        name (str): Image Name

    Returns:
        bytes: Image Data

    Raises:
        FileNotFoundError: File does not exist
    """

def delete(name:str):
    """

    Args:
        name (str): [description]
    """


def downscale(image:bytes,target:int) -> bytes:
    """Downscales an image into

    Args:
        image (bytes): Image Data
        target (int): Target Megapixels

    Returns:
        bytes: [description]

    Raises:
        ValueError: Invalid Image Data
    """

import os as _os
if _os.getenv('IMAGE_STORAGE') == "S3":
    from .s3 import put,get,delete
elif _os.getenv('IMAGE_STORAGE') == "LOCAL":
    from .local import put,get,delete

from . import local as _local,s3 as _s3
from .image import downscale,encodeToJPEG