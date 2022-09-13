from modules import schemas, encoding, database, encoding, store, settings
from modules.downloaders.utils import normalise_tags
from modules.tags import generate_ai_tags
import base64
import mimetypes
import hashlib
from typing import Union


async def generate(data:bytes,filename:str,
        use_ai_tags:bool=settings.TAGS_TAGGING_SERVICE_ENABLED,
        uploader_id:Union[int,None] = None,
        additional_tags:Union[list[str],None] = None,
        source:Union[str,None] = None,
        rating:Union[str,None] = None,
        ) -> schemas.Post:
    post = await encode_post(data,filename)
    
    
    if additional_tags:
        additional_tags = normalise_tags(additional_tags)
        tags = set(post.tags + additional_tags)
        post.tags = list(tags)
    if uploader_id:
        post.uploader = uploader_id
    if source:
        post.source = source
    if rating:
        post.rating = rating # type: ignore

    if use_ai_tags:
        mimetype,_ = mimetypes.guess_type(filename)
        if mimetype != None:
            tags = generate_ai_tags(data,filename,mimetype)
            post.tags = list(set(post.tags + tags))
    
    return post


async def encode_post(data:bytes,filename:str):
    hashes = schemas.Hashes()
    
    media_type = await encoding.predict_media_type(data,filename)
    with media_type(data) as media:
        full = media.full()
        preview = media.preview()
        thumbnail = media.thumbnail()
    
    _generate_hashes(hashes, data)
    full_schema = process_file(full, hashes)
    preview_schema = process_file(preview, hashes) if preview else None
    thumbnail_schema = process_file(thumbnail, hashes)
    
    return schemas.Post(
        id=database.Post.generate_id(),
        tags=[media_type.type],
        hashes=hashes,
        full=full_schema, # type: ignore
        preview=preview_schema, # type: ignore
        thumbnail=thumbnail_schema, # type: ignore
        media_type=media_type.type,
    )


def process_file(file:encoding.GenericFile, hashes: schemas.Hashes) -> schemas.GenericMedia:
    _generate_hashes(hashes, file.data)
    filename = _generate_filename(file)
    _save_file(file.data,filename)
    url = store.generate_generic_url(filename)
    schema = _generate_schema(file,url)
    return schema


def _save_file(data:bytes,filename:str):
    try:
        store.put(data,filename)
    except FileExistsError:
        store.delete(filename)
        store.put(data,filename)


def _generate_hashes(hashes: schemas.Hashes, data:bytes):
    hashes.md5s.append(hashlib.md5(data).digest())
    hashes.sha256s.append(hashlib.sha256(data).digest())


def _generate_schema(file:encoding.GenericFile,url:str) -> schemas.GenericMedia:
    if isinstance(file,encoding.ImageFile):
        return schemas.Image(
            url=url,
            mimetype=file.mimetype,
            height=file.height,
            width=file.width,
        )
    elif isinstance(file,encoding.AnimationFile):
        return schemas.Animation(
            url=url,
            mimetype=file.mimetype,
            height=file.height,
            width=file.width,
            duration=file.duration,
            frame_count=file.frame_count,
            )
    elif isinstance(file,encoding.VideoFile):
        return schemas.Video(
            url=url,
            mimetype=file.mimetype,
            height=file.height,
            width=file.width,
            duration=file.duration,
            fps=file.framerate,
            has_sound=file.hasAudio,
            )
    else:
        raise TypeError("Unknown file type")


def _generate_filename(file:encoding.GenericFile) -> str:
    hash_bytes = hashlib.sha3_256(file.data).digest()
    hash = base64.urlsafe_b64encode(hash_bytes).decode()
    hash = hash[:10]
    
    ext = mimetypes.guess_extension(file.mimetype) or ""
    filename = hash + ext
    return filename
