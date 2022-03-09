from modules import settings
from . import ImageFile,BaseMedia,Dimensions
from dataclasses import dataclass
from typing_extensions import Self
import io
from PIL import Image as PILImage


@dataclass
class Image(BaseMedia):
    type="image"
    PIL:PILImage.Image
    dimensions:Dimensions

    @classmethod
    def from_pillow(cls,pillow:PILImage.Image) -> Self:
        dimensions = Dimensions(pillow.width,pillow.height)
        return Image(
            PIL = pillow,
            dimensions = dimensions,
        )
    
    @classmethod
    async def from_bytes(cls,data:bytes) -> Self:
        """Raises:
        - ValueError: Image is too big to process
        - ValueError: Could not Load Image
        """
        PILImage.MAX_IMAGE_PIXELS = (5000*5000) * 2
        # Prevent large images performance impact
        # x2 because error is only raised on x2 max pixels
        buf = io.BytesIO(data)
        try:
            # formats=None means attempt to load all formats
            pil_img = PILImage.open(buf,formats=None)
        except PILImage.DecompressionBombError:
            raise ValueError("Image is too big to process")
        except Exception:
            raise ValueError("Could not Load Image")
        else:
            return Image.from_pillow(pil_img)


    async def full(self) -> ImageFile:
        config = settings.get('encoding.image.full')
        return self._process_using_config(config)


    async def preview(self) -> ImageFile:
        config = settings.get('encoding.image.preview')
        return self._process_using_config(config)


    async def thumbnail(self) -> ImageFile:
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
        res = _calculate_downscale(self.dimensions,target)
        (
            self.PIL
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