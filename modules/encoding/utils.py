from . import AnimationEncoder, ImageEncoder, VideoEncoder, probe, BaseEncoder, GenericFile
from modules import schemas

import mimetypes
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('image/apng', '.apng')


OriginalFile = GenericFile
ThumbnailFile = GenericFile


async def encode_media(data: bytes, filename: str) -> tuple[OriginalFile, ThumbnailFile, list[GenericFile]]:
    encoder = await generate_encoder(data, filename)
    original = encoder.original()
    thumbnail = encoder.thumbnail()
    
    medias = []
    medias.append(original)
    medias.append(thumbnail)
    preview = encoder.preview()
    if preview:
        medias.append(preview)

    return original, thumbnail, medias


async def generate_encoder(data: bytes, filename: str) -> BaseEncoder:
    """Raises:
    - ValueError: Filetype not supported
    """
    mime: str = mimetypes.guess_type(filename)[0]  # type: ignore
    type, subtype = mime.split('/')

    if subtype in {"webp", "gif", "apng"}:
        if probe.is_animated_sequence(data):
            return AnimationEncoder(data)
        else:
            return ImageEncoder(data)
    elif type == 'image':
        return ImageEncoder(data)
    elif type == 'video':
        return VideoEncoder(data)
    else:
        raise ValueError(f'Filetype not supported: {mime}')
