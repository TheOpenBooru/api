from . import BaseEncoder, ImageFile, probe
from dataclasses import dataclass
from openbooru.modules import settings, schemas
from pydantic import BaseModel
from PIL import Image as PILImage
import io


@dataclass
class Dimensions:
    x: int
    y: int


class ImageEncodingConfig(BaseModel):
    width: int
    height: int
    quality: int = 100
    lossless: bool = False


class ImageEncoder(BaseEncoder):
    data: bytes
    type = schemas.MediaType.image
    pillow: PILImage.Image

    def __init__(self, data: bytes):
        """Raises:
        - ValueError: Image is too big to process
        - ValueError: Could not Load Image
        """
        # Set max acceptable image size to prevent DOS
        PILImage.MAX_IMAGE_PIXELS = (
            settings.IMAGE_FULL_HEIGHT * settings.IMAGE_FULL_HEIGHT)

        buf = io.BytesIO(data)
        try:
            # formats=None means attempt to load all formats
            pil_img = PILImage.open(buf, formats=None)
        except PILImage.DecompressionBombError:
            raise ValueError("Image is too big to process")
        except Exception as e:
            raise ValueError(str(e))

        self.pillow = pil_img
        self.data = data

    def original(self) -> ImageFile:
        probe.guess_mimetype(self.data)
        return self.process(
            ImageEncodingConfig(
                width=settings.IMAGE_FULL_WIDTH,
                height=settings.IMAGE_FULL_HEIGHT,
                quality=settings.IMAGE_FULL_QUALITY,
                lossless=settings.IMAGE_FULL_LOSSLESS,
            )
        )

    def preview(self) -> ImageFile:
        return self.process(
            ImageEncodingConfig(
                width=settings.IMAGE_PREVIEW_HEIGHT,
                height=settings.IMAGE_PREVIEW_HEIGHT,
                quality=settings.IMAGE_PREVIEW_QUALITY,
                lossless=settings.IMAGE_PREVIEW_LOSSLESS,
            )
        )
    
    def thumbnail(self) -> ImageFile:
        return self.process(
            ImageEncodingConfig(
                width=settings.THUMBNAIL_WIDTH,
                height=settings.THUMBNAIL_HEIGHT,
                quality=settings.THUMBNAIL_QUALITY,
                lossless=settings.THUMBNAIL_LOSSLESS,
            )
        )

    def process(self, config: ImageEncodingConfig) -> ImageFile:
        actual_size = Dimensions(self.pillow.width, self.pillow.height)
        target_size = Dimensions(config.width, config.height)
        size = calculate_downscale(actual_size, target_size)

        buf = io.BytesIO()
        (
            self.pillow
            .resize((size.x, size.y), PILImage.LANCZOS)
            .save(
                fp=buf,
                format='webp',
                quality=config.quality,
                lossless=config.lossless
            )
        )
        data = buf.getvalue()

        return ImageFile(
            data=data,
            mimetype='image/webp',
            width=size.x,
            height=size.y,
        )



def calculate_downscale(resolution: Dimensions, target: Dimensions) -> Dimensions:
    biggest_factor = max(
        1,
        resolution.x / target.x,
        resolution.y / target.y,
    )

    output_width = int(resolution.x / biggest_factor)
    output_height = int(resolution.y / biggest_factor)

    return Dimensions(output_width, output_height)
