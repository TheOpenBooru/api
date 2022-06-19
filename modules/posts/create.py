from modules import schemas,encoding,database,encoding,store
import mimetypes
import hashlib
from typing import Union


class PostExistsException(Exception):
    pass


async def create(
        data:bytes,
        filename:str,
        *,
        user_id:Union[int,None] = None,
        additional_tags:Union[list[str],None] = None,
        source:Union[str,None] = None,
        ) -> schemas.Post:
    generator = _PostSchemaGenerator(data,filename)
    schema = await generator.generate()
    
    if additional_tags:
        schema.tags.extend(additional_tags)
    if user_id:
        schema.uploader = user_id
    if source:
        schema.source = source
    
    database.Post.create(schema)
    return schema

class _PostSchemaGenerator:
    def __init__(self,data:bytes,filename:str):
        self.data = data
        self.filename = filename
        self.md5s = []
        self.sha256s = []
    
    
    async def generate(self):
        if await _checkExists(self.data):
            raise PostExistsException
        
        media_type = await encoding.predict_media_type(self.data,self.filename)
        with media_type(self.data) as media:
            full = media.full()
            preview = media.preview()
            thumbnail = media.thumbnail()
        
        self._generate_hashes(self.data)
        full_schema = self.process_file(full)
        preview_schema = self.process_file(preview) if preview else None
        thumbnail_schema = self.process_file(thumbnail)
        
        return schemas.Post(
            id=database.Post.get_unused_id(),
            md5s=self.md5s,
            uploader=0,
            sha256s=self.sha256s,
            full=full_schema, # type: ignore
            preview=preview_schema, # type: ignore
            thumbnail=thumbnail_schema, # type: ignore
            media_type=media_type.type,
        )
    
    
    def process_file(self,file:encoding.GenericFile) -> schemas.GenericMedia:
        self._generate_hashes(file.data)
        filename = _generate_filename(file)
        store.put(file.data,filename)
        url = store.generate_generic_url(filename)
        schema = _generate_schema(file,url)
        return schema
    
    
    
    def _generate_hashes(self,data:bytes):
        self.md5s.append(hashlib.md5(data).hexdigest())
        self.sha256s.append(hashlib.sha256(data).hexdigest())


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
    hash = hashlib.sha3_256(file.data).hexdigest()
    ext = mimetypes.guess_extension(file.mimetype) or ""
    filename = hash + ext
    return filename


async def _checkExists(data:bytes) -> bool:
    md5 = hashlib.md5(data).hexdigest()
    try:
        database.Post.getByMD5(md5)
    except KeyError:
        return False
    else:
        return True