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
    md5:str
    sha3_256:str
    _pillow:PILImage.Image
    def __init__(self,data:bytes):
        self._pillow = pil_image = _bytes_to_pillow(data)
        self.resolution = Dimensions(pil_image.width,pil_image.height)
        
        buf = io.BytesIO()
        pil_image.save(buf,format='WEBP',lossless=True)
        self.data = buf.read()
        self.md5 = hashlib.md5(self.data).hexdigest()
        self.sha3_256 = hashlib.sha3_256(self.data).hexdigest()


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
    pil_img = _bytes_to_pillow(image.data)
    pil_img = pil_img.resize(resolution.to_tuple(),PILImage.LANCZOS)
    image_bytes = pil_img.tobytes('raw')
    finalImage = Image(image_bytes)
    return finalImage


def _bytes_to_pillow(data:bytes) -> PILImage.Image:
    image_buf = io.BytesIO(data)
    pil_image = PILImage.open(image_buf)
    pil_image.verify()
    return pil_image
