from modules import settings
import io
import hashlib
from dataclasses import dataclass
from PIL import Image as PILImage

@dataclass
class Dimensions:
    width:int
    height:int
    def to_tuple(self) -> tuple[int,int]:
        return self.width,self.height

class Image:
    width:int
    height:int
    data:bytes
    pillow:PILImage.Image
    def __init__(self,data:bytes,format:str):
        buf = io.BytesIO(data)
        self.pillow = pil_img = PILImage.open(buf,formats=[format])
        self.resolution = Dimensions(pil_img.width,pil_img.height)
        
        buf = io.BytesIO()
        pil_img.save(buf,format='WEBP',lossless=True)
        self.data = buf.read()


def generateThumbnail(image:Image) -> Image:
    config = settings.get('settings.posts.thumbnail')
    return _process_from_config(image,config)


def generatePreview(image:Image) -> Image:
    config = settings.get('settings.posts.preview')
    return _process_from_config(image,config)


def _process_from_config(image:Image,config:dict) -> Image:
    target = Dimensions(config['width'],config['height'])
    quality = config['quality']
    res = calculate_downscale(image.resolution,target)
    output_image = process(image,res,quality)
    return output_image


def calculate_downscale(resolution:Dimensions,target:Dimensions) -> Dimensions:
    output = Dimensions(resolution.width,resolution.height)
    possible_factors = (
        1.0,
        output.width / target.width,
        output.height / target.height
    )
    factor = max(possible_factors)
    output.width = int(output.width // factor)
    output.height = int(output.height // factor)
    return output


def process(image:Image,resolution:Dimensions,quality:int=95):
    pil_img = image.pillow
    pil_img = pil_img.resize(resolution.to_tuple(),PILImage.LANCZOS)
    image_bytes = pil_img.tobytes('raw')
    finalImage = Image(image_bytes,'webp')
    return finalImage
