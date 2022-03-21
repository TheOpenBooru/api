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
            type=media_type.type,
        )

    def process_file(self,file:encoding.GenericFile) -> schemas.Image:
        self._generate_hashes(file)
        ext = mimetypes.guess_extension(file.mimetype) or ""
        key = store.put(file.data,suffix=ext)
        return schemas.Image(
            url=store.url(key),
            mimetype=file.mimetype,
            height=file.height,
            width=file.width
        )

    def _generate_hashes(self,file:encoding.GenericFile):
        data = file.data
        self.md5s.append(hashlib.md5(data).hexdigest())
        self.sha3_256.append(hashlib.sha3_256(data).hexdigest())

# Generate Schema
    # Process Media
    # Store Media
# Insert into DB