from modules import settings
from dataclasses import dataclass
import io
import numpy as np
from PIL import Image as PILImage
import cv2

@dataclass(frozen=True)
class Image:
    data:bytes
    format:str
    width:int
    height:int

def generateImageEncodings(img:Image) -> tuple[Image,Image,Image]:
    """Generate downscaled versions of an image

    Args:
    - img (Image): The Image Data

    Returns:
    - Full Image (Image)
    - Preview Image (Image)
    - Thumbnail Image (Image)
    """
    config = settings.get('settings.posts')
    
    fullImage = encode(
        img,(config['full']['max_width'],config['full']['max_height']),
        config['full']['quality'],
    )
    previewImage = encode(
        img,(config['preview']['max_width'],config['preview']['max_height']),
        config['preview']['quality'],
    )
    thumbnailImage = encode(
        img,(config['thumbnail']['max_width'],config['thumbnail']['max_height']),
        config['thumbnail']['quality']
    )
    return fullImage,previewImage,thumbnailImage

def calculateDownscale(dimensions:tuple[int,int],target:tuple[int,int]) -> tuple[int,int]:
    ...


def encode(input:Image,target:tuple[int,int],quality:int=100) -> Image:
    """Raises:
    - ValueError: Invalid Image Data
    - ValueError: Could not parse image
    """
    buf = io.BytesIO(input.data)
    pillowImage = PILImage.open(buf).convert('RGBA')
    pillowImage = pillowImage.resize(target,PILImage.ANTIALIAS)
    
    numpyImage = np.array(pillowImage)
    suc, imageBuffer = cv2.imencode(".webp",numpyImage, [cv2.IMWRITE_WEBP_QUALITY, quality])
    if not suc:
        raise ValueError("Could not parse image")
    data = imageBuffer.tobytes()
    finalImage = Image(data,'webp',*target)
    return finalImage

def getImageData(filename:str,img:bytes) -> Image:
    """Raises:
    - ValueError: Invalid Image Data

    Returns:
        int: Width
        int: Height
        str: Image Format
    """
    raise NotImplementedError