from . import BaseMedia,ImageFile,Dimensions
from modules import settings, schemas
from typing_extensions import Self
from dataclasses import dataclass
from PIL import Image as PILImage
import io


@dataclass
class Image(BaseMedia):
    type = schemas.MediaType.image
    pillow:PILImage.Image
    _dimensions:Dimensions


    def __init__(self,data:bytes):
        self._data = data

    def __enter__(self) -> Self:
        """Raises:
        - ValueError: Image is too big to process
        - ValueError: Could not Load Image
        """
        # Set max acceptable image size to prevent DOS
        PILImage.MAX_IMAGE_PIXELS = (settings.IMAGE_FULL_HEIGHT * settings.IMAGE_FULL_HEIGHT)
        
        buf = io.BytesIO(self._data)
        try:
            # formats=None means attempt to load all formats
            pil_img = PILImage.open(buf,formats=None)
        except PILImage.DecompressionBombError:
            raise ValueError("Image is too big to process")
        except Exception as e:
            raise ValueError(str(e))
        
        self._dimensions = Dimensions(pil_img.width,pil_img.height)
        self.pillow = pil_img
        return self


    def __exit__(self, exception_type, exception_value, traceback):
        ...


    def full(self) -> ImageFile:
        return self._process(
            Dimensions(settings.IMAGE_FULL_WIDTH,settings.IMAGE_FULL_HEIGHT),
            settings.IMAGE_FULL_QUALITY,
            settings.IMAGE_FULL_LOSSLESS,
        )


    def preview(self) -> ImageFile:
        return self._process(
            Dimensions(settings.IMAGE_PREVIEW_WIDTH,settings.IMAGE_PREVIEW_HEIGHT),
            settings.IMAGE_PREVIEW_QUALITY,
            settings.IMAGE_PREVIEW_LOSSLESS,
        )


    def thumbnail(self) -> ImageFile:
        return self._process(
            Dimensions(settings.THUMBNAIL_WIDTH,settings.THUMBNAIL_HEIGHT),
            settings.THUMBNAIL_QUALITY,
            settings.THUMBNAIL_LOSSLESS,
        )


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
            self.pillow
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