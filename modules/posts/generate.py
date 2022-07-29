from modules import schemas, encoding, database, encoding, store, settings
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
    generator = PostEncoder(data,filename)
    post = await generator.generate()
    
    if additional_tags:
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


class PostEncoder:
    def __init__(self,data:bytes,filename:str):
        self.data = data
        self.filename = filename
        self.hashes = schemas.Hashes()
    
    
    async def generate(self):
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
            id=database.Post.get_new_id(),
            tags=[media_type.type],
            hashes=self.hashes,
            full=full_schema, # type: ignore
            preview=preview_schema, # type: ignore
            thumbnail=thumbnail_schema, # type: ignore
            media_type=media_type.type,
        )
    
    
    def process_file(self,file:encoding.GenericFile) -> schemas.GenericMedia:
        self._generate_hashes(file.data)
        filename = _generate_filename(file)
        self._save_file(file.data,filename)
        url = store.generate_generic_url(filename)
        schema = _generate_schema(file,url)
        return schema


    def _save_file(self,data:bytes,filename:str):
        try:
            store.put(data,filename)
        except FileExistsError:
            store.delete(filename)
            store.put(data,filename)
    
    
    def _generate_hashes(self,data:bytes):
        self.hashes.md5s.append(hashlib.md5(data).hexdigest())
        self.hashes.sha256s.append(hashlib.sha256(data).hexdigest())


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
