import mimetypes
from modules import schemas,encoding,database,store,encoding
from modules.encoding import GenericFile,GenericMedia
import hashlib


async def create(data:bytes,filename:str) -> schemas.Post:
    generator = _PostSchemaGenerator(data,filename)
    schema = await generator.generate()
    database.Post.create(schema)
    return schema


class _PostSchemaGenerator:
    def __init__(self,data:bytes,filename:str):
        self.data = data
        self.filename = filename
        self.md5s = []
        self.sha3_256 = []

    async def generate(self):
        media_type = await encoding.predict_media_type(self.data,self.filename)
        with media_type(self.data) as media:
            full = media.full()
            preview = media.preview()
            thumbnail = media.thumbnail()
        
        full_schema = self.process_file(full)
        preview_schema = self.process_file(preview) if preview else None
        thumbnail_schema = self.process_file(thumbnail)

        return schemas.Post(
            id=database.Post.get_unused_id(),
            md5s=self.md5s,
            uploader=0,
            sha256s=self.sha3_256,
            full=full_schema, # type: ignore
            preview=preview_schema, # type: ignore
            thumbnail=thumbnail_schema, # type: ignore
            media_type=media_type.type,
        )

    def process_file(self,file:encoding.GenericFile) -> schemas.GenericMedia:
        self._generate_hashes(file)
        ext = mimetypes.guess_extension(file.mimetype) or ""
        key = store.put(file.data,suffix=ext)
        url = store.url(key)
        schema = self._generate_schema(file,url)
        return schema
    

    def _generate_schema(self,file:encoding.GenericFile,url:str) -> schemas.GenericMedia:
        if isinstance(file,encoding.ImageFile):
            return schemas.Image(
                url=url,
                mimetype=file.mimetype,
                height=file.height,
                width=file.width,
                type="animation"
            )
        elif isinstance(file,encoding.AnimationFile):
            return schemas.Animation(
                url=url,
                mimetype=file.mimetype,
                height=file.height,
                width=file.width,
                duration=file.duration,
                frame_count=file.frame_count,
                type="animation"
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
                type="video"
                )
        else:
            raise TypeError("Unknown file type")
    
    def _generate_hashes(self,file:encoding.GenericFile):
        data = file.data
        self.md5s.append(hashlib.md5(data).hexdigest())
        self.sha3_256.append(hashlib.sha3_256(data).hexdigest())
