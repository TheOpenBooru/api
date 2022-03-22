from . import GenericMedia,Animation,Image,Video
from .animation import isAnimatedSequence

import mimetypes
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/apng', '.apng')

async def predict_media_type(data:bytes,filename:str) -> type[GenericMedia]:
    """Raises:
    - ValueError: Filetype not supported
    """
    mime:str = mimetypes.guess_type(filename)[0] # type: ignore
    type,subtype = mime.split('/')

    if subtype in {"webp","gif","apng"}:
        if isAnimatedSequence(data):
            return Animation
        else:
            return Image
    elif type == 'image':
        return Image
    elif type == 'video':
        return Video
    else:
        raise ValueError(f'Filetype not supported: {mime}')
