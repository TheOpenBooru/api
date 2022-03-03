from sys import prefix
from . import router
from modules import database,store,schemas,encoding
import hashlib
import mimetypes
mimetypes.add_type('image/webp','.webp')
from fastapi import Response,status,UploadFile 

@router.post("/create")
async def create_post(image_file:UploadFile):
    constructor = PostConstructor()
    try:
        post = await constructor.generate_post(image_file)
    except ValueError as e:
        reason = constructor.error_message or "Unknown"
        return Response(reason,status_code=status.HTTP_400_BAD_REQUEST)
    try:
        database.Post.create(post)
    except ValueError:
        return Response("Post already exists",status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status_code=status.HTTP_201_CREATED)
        

GenericFile = encoding.ImageFile | encoding.AnimationFile | encoding.VideoFile
GenericSchema = schemas.Image | schemas.Video | schemas.Animation

class PostConstructor:
    error_message:str
    md5s:list[str]
    sha3_256s:list[str]
    def __init__(self):
        self.md5s = []
        self.sha3_256s = []
    
    async def generate_post(self,image_file:UploadFile) -> schemas.Post:
        data:bytes = await image_file.read() # type: ignore
        media_type = await encoding.generate_media(data,image_file.filename)
        media = await media_type.from_bytes(data)
        
        full_image = await media.full()
        preview_image = await media.preview()
        thumbnail_image = await media.thumbnail()
        
        full = await self._process_media("full",full_image)
        thumbnail = await self._process_media("thumbnail",thumbnail_image)
        if preview_image:
            preview = await self._process_media("preview",preview_image)
        else:
            preview = None

        postID = database.Post.get_unused_id()
        return schemas.Post(
            id=postID,uploader=1,type=media_type.type,
            full=full,preview=preview,thumbnail=thumbnail, # type: ignore
            md5s=self.md5s,sha256s=self.sha3_256s,
        )


    async def _process_media(self,type:str,media:GenericFile) -> GenericSchema:
        store_url = self._store_file(type,media)
        self._generate_hashes(media)
        return self._generate_schema(media,store_url)


    def _store_file(self,type:str,media:GenericFile) -> str:
        ext:str = mimetypes.guess_extension(media.mimetype) # type: ignore
        key = store.put(media.data,prefix=type,suffix=ext)
        return store.url(key)


    def _generate_hashes(self,data:GenericFile) -> None:
        md5 = hashlib.md5(data.data).hexdigest()
        sha3 = hashlib.sha3_256(data.data).hexdigest()
        self.md5s.append(md5)
        self.sha3_256s.append(sha3)


    def _generate_schema(self,file:GenericFile,url) -> GenericSchema:
        if isinstance(file,encoding.ImageFile):
            schema = schemas.Image(
                url=url,
                mimetype=file.mimetype,
                width=file.width,
                height=file.height,
            )
        elif isinstance(file,encoding.AnimationFile):
            schema = schemas.Animation(
                url=url,
                mimetype=file.mimetype,
                width=file.width,
                height=file.height,
                duration=file.duration,
                frame_count=file.frame_count,
            )
        elif isinstance(file,encoding.VideoFile):
            schema = schemas.Video(
                url=url,
                mimetype=file.mimetype,
                width=file.width,
                height=file.height,
                duration=file.duration,
                fps=file.framerate,
                frame_count=file.frame_count,
                has_sound=file.hasAudio,
            )
        
        return schema