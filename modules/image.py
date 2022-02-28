import os
from modules import settings
import io
import hashlib
from dataclasses import dataclass
from PIL import Image as PILImage

@dataclass(frozen=True)
class Dimensions:
    width:int
    height:int
    def to_tuple(self) -> tuple[int,int]:
        return self.width,self.height

@dataclass(frozen=True)
class Image:
    data:bytes
    format:str
    resolution:Dimensions
    pil_img:PILImage.Image


def file_to_image(file:io.BytesIO | io.BufferedReader) -> Image:
    """Raises:
        ValueError: Could not Load Image
    """
    data = file.read()
    buf = io.BytesIO(data)
    try:
        pil_img = PILImage.open(buf,formats=['png','webp','jpeg'])
    except:
        raise ValueError("Could not Load Image")
    
    res = Dimensions(pil_img.width,pil_img.height)
    return Image(
        data = data,
        resolution = res,
        format = pil_img.format,
        pil_img = pil_img,
    )


def generateFull(image:Image) -> Image:
    config = settings.get('settings.posts.full')
    return _process_using_config(image,config)


def generateThumbnail(image:Image) -> Image:
    config = settings.get('settings.posts.thumbnail')
    return _process_using_config(image,config)


def generatePreview(image:Image) -> Image:
    config = settings.get('settings.posts.preview')
    return _process_using_config(image,config)


def _process_using_config(image:Image,config:dict) -> Image:
    target = Dimensions(config['max_width'],config['max_width'])
    quality = config['quality']
    res = calculate_downscale(image.resolution,target)
    output_image = process(image,res,quality)
    return output_image


def calculate_downscale(resolution:Dimensions,target:Dimensions) -> Dimensions:
    possible_factors = (
        1.0,
        resolution.width / target.width,
        resolution.height / target.height
    )
    limiting_factor = max(possible_factors)
    output_width = int(resolution.width / limiting_factor)
    output_height = int(resolution.height / limiting_factor)
    return Dimensions(output_width,output_height)


def process(image:Image,resolution:Dimensions,quality:int) -> Image:
    pil_img = image.pil_img
    pil_img = pil_img.resize(resolution.to_tuple(),PILImage.LANCZOS)
    buf = io.BytesIO()
    pil_img.save(buf,format='WEBP',quality=quality)
    return Image(
        data = buf.getvalue(),
        format='WEBP',
        resolution = (resolution),
        pil_img = pil_img
        )

def _pillow_to_webp_data(pillow_img:PILImage.Image) -> bytes:
    buf = io.BytesIO()
    pillow_img.save(buf,format='WEBP',lossless=True)
    return buf.read()
