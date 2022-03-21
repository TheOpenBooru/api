from functools import cache
import os
import random
from typing_extensions import Self
from . import BaseMedia,ImageFile,Dimensions
from modules import settings
from dataclasses import dataclass
from PIL import Image as PILImage
import io

# Prevent large images performance impact
# x2 because error is only raised on x2 max pixels
PILImage.MAX_IMAGE_PIXELS = (5000*5000) * 2

@dataclass
class Image(BaseMedia):
    type="image"
    _PIL:PILImage.Image
    _dimensions:Dimensions


    def __init__(self,data:bytes):
        """Raises:
        - ValueError: Image is too big to process
        - ValueError: Could not Load Image
        """
        self._data = data

    def __enter__(self) -> Self:
        buf = io.BytesIO(self._data)
        try:
            # formats=None means attempt to load all formats
            pil_img = PILImage.open(buf,formats=None)
        except PILImage.DecompressionBombError:
            raise ValueError("Image is too big to process")
        except Exception as e:
            raise ValueError(str(e))
        
        self._dimensions = Dimensions(pil_img.width,pil_img.height)
        self._PIL = pil_img
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        ...


    def full(self) -> ImageFile:
        config = settings.get('encoding.image.full')
        return self._process_using_config(config)


    def preview(self) -> ImageFile:
        config = settings.get('encoding.image.preview')
        return self._process_using_config(config)


    def thumbnail(self) -> ImageFile:
        config = settings.get('encoding.image.thumbnail')
        return self._process_using_config(config)
    

    def _process_using_config(self,config:dict) -> ImageFile:
        dimensions = Dimensions(config['max_width'],config['max_height'])
        return self._process(
            dimensions,
            config['quality'],
            config['lossless'],
        )


    def _process(self,target:Dimensions,quality:int,lossless:bool=False) -> ImageFile:
        output_buf = io.BytesIO()
        res = _calculate_downscale(self._dimensions,target)
        (
            self._PIL
            .resize((res.width,res.height),PILImage.LANCZOS)
            .save(output_buf,format='webp',quality=quality,lossless=lossless)
        )
        return ImageFile(
            data=output_buf.getvalue(),
            mimetype='image/webp',
            width=res.width,
            height=res.height
        )

def _calculate_downscale(resolution:Dimensions,target:Dimensions) -> Dimensions:
    downscale_factors = (
        1.0,
        resolution.width / target.width,
        resolution.height / target.height,
    )
    limiting_factor = max(downscale_factors)
    output_width = int(resolution.width / limiting_factor)
    output_height = int(resolution.height / limiting_factor)
    return Dimensions(output_width,output_height)