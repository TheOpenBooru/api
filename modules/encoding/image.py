from . import BaseMedia,ImageFile,Dimensions
from modules import settings, schemas
from typing_extensions import Self
from dataclasses import dataclass
from PIL import Image as PILImage
import io


class Image(BaseMedia):
    type = schemas.MediaType.image
    pillow:PILImage.Image


    def __init__(self,data:bytes):
        """Raises:
        - ValueError: Image is too big to process
        - ValueError: Could not Load Image
        """
        # Set max acceptable image size to prevent DOS
        PILImage.MAX_IMAGE_PIXELS = (settings.IMAGE_FULL_HEIGHT * settings.IMAGE_FULL_HEIGHT)
        
        buf = io.BytesIO(data)
        try:
            # formats=None means attempt to load all formats
            pil_img = PILImage.open(buf,formats=None)
        except PILImage.DecompressionBombError:
            raise ValueError("Image is too big to process")
        except Exception as e:
            raise ValueError(str(e))
        
        self.pillow = pil_img


    def full(self) -> ImageFile:
        return process(
            self.pillow,
            Dimensions(settings.IMAGE_FULL_WIDTH,settings.IMAGE_FULL_HEIGHT),
            settings.IMAGE_FULL_QUALITY,
            settings.IMAGE_FULL_LOSSLESS,
        )


    def preview(self) -> ImageFile:
        return process(
            self.pillow,
            Dimensions(settings.IMAGE_PREVIEW_WIDTH,settings.IMAGE_PREVIEW_HEIGHT),
            settings.IMAGE_PREVIEW_QUALITY,
            settings.IMAGE_PREVIEW_LOSSLESS,
        )


    def thumbnail(self) -> ImageFile:
        return process(
            self.pillow,
            Dimensions(settings.THUMBNAIL_WIDTH,settings.THUMBNAIL_HEIGHT),
            settings.THUMBNAIL_QUALITY,
            settings.THUMBNAIL_LOSSLESS,
        )


def process(pillow:PILImage.Image,target:Dimensions,quality:int,lossless:bool=False) -> ImageFile:
    output_buf = io.BytesIO()
    dimensions = Dimensions(pillow.width, pillow.height)
    output_res = calculate_downscale(dimensions,target)
    (
        pillow
        .resize(output_res, PILImage.LANCZOS)
        .save(output_buf,
              format='webp',
              quality=quality,
              lossless=lossless
        )
    )
    return ImageFile(
        data=output_buf.getvalue(),
        mimetype='image/webp',
        width=output_res.x,
        height=output_res.y,
    )


def calculate_downscale(resolution: Dimensions,target: Dimensions) -> Dimensions:
    downscale_factors = (
        1.0,
        resolution.x / target.x,
        resolution.y / target.y,
    )
    limiting_factor = max(downscale_factors)
    
    output_width = int(resolution.x / limiting_factor)
    output_height = int(resolution.y / limiting_factor)
    
    return Dimensions(output_width,output_height)