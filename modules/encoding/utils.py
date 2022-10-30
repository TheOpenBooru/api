from modules.encoding.probe import isAnimatedSequence
from . import GenericMedia,Animation,Image,Video, isAnimatedSequence

import mimetypes
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/apng', '.apng')


async def generate_media(data:bytes,filename:str) -> GenericMedia:
    """Raises:
    - ValueError: Filetype not supported
    """
    mime:str = mimetypes.guess_type(filename)[0] # type: ignore
    type,subtype = mime.split('/')

    if subtype in {"webp","gif","apng"}:
        if isAnimatedSequence(data):
            return Animation(data)
        else:
            return Image(data)
    elif type == 'image':
        return Image(data)
    elif type == 'video':
        return Video(data)
    else:
        raise ValueError(f'Filetype not supported: {mime}')
