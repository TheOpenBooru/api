from . import BaseMedia,Animation,Image,Video,Dimensions
from PIL import Image as PILImage

import io
import mimetypes
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/apng', '.apng')


async def predict_media_type(data:bytes,filename:str) -> type[BaseMedia]:
    """Raises:
    - ValueError: Filetype not supported
    """
    mime:str = mimetypes.guess_type(filename)[0] # type: ignore
    type,subtype = mime.split('/')

    if subtype in {"webp","gif","apng"}:
        if _isAnimatedSequence(data):
            return Animation
        else:
            return Image
    elif type == 'video':
        return Video
    elif type == 'image':
        return Image
    else:
        raise ValueError(f'Filetype not supported: {mime}')


def _isAnimatedSequence(data:bytes) -> bool:
    buf = io.BytesIO(data)
    pil_img = PILImage.open(buf,formats=None)
    return pil_img.is_animated


def calculate_downscale(resolution:Dimensions,target:Dimensions) -> Dimensions:
    downscale_factors = (
        1.0,
        resolution.width / target.width,
        resolution.height / target.height,
    )
    limiting_factor = max(downscale_factors)
    output_width = int(resolution.width / limiting_factor)
    output_height = int(resolution.height / limiting_factor)
    return Dimensions(output_width,output_height)
