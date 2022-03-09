from . import router
from modules import database,store,schemas,encoding
from fastapi import Response,status,UploadFile 
import hashlib
import mimetypes
mimetypes.add_type('image/webp','.webp')

@router.post("/create")
async def create_post(image_file:UploadFile):
    constructor = PostConstructor()
    try:
        post = await constructor.construct(image_file)
    except Exception:
        return Response(constructor.error_message,status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return post


GenericSchema = schemas.Image | schemas.Video | schemas.Animation

class PostConstructor:
    error_message:str = "Unknown Error"
    md5s:list[str]
    sha3_256s:list[str]
    def __init__(self):
        self.md5s = []
        self.sha3_256s = []

    
    async def construct(self,image_file:UploadFile) -> schemas.Post:
        media_type, media = await self._generate_media(image_file)
        post = await self._generate_post_schema(media_type, media)
        self._insert_post_into_database(post)
        return post


    def _log_and_raise_error(self,message,exception):
        self.error_message = message
        raise exception(message)
    
    async def _generate_media(self, image_file):
        data:bytes = await image_file.read() # type: ignore
        try:
            media_type = await encoding.predict_media_type(data,image_file.filename)
        except Exception as e:
            self._log_and_raise_error("Could not predict media type",e)
        media = await media_type.from_bytes(data)
        return media_type,media

    def _insert_post_into_database(self, post:schemas.Post):
        try:
            database.Post.create(post)
        except KeyError as e:
            self._log_and_raise_error("Post already exists",e)

    async def _generate_post_schema(self, media_type:type[encoding.BaseMedia], media) -> schemas.Post:
        full_image = await media.full()
        preview_image = await media.preview()
        thumbnail_image = await media.thumbnail()
        
        full = await self._process_media("full",full_image)
        thumbnail = await self._process_media("thumbnail",thumbnail_image)
        preview = await self._process_media("preview",preview_image)

        postID = database.Post.get_unused_id()
        post = schemas.Post(
            id=postID,uploader=1,type=media_type.type,
            full=full,preview=preview,thumbnail=thumbnail, # type: ignore
            md5s=self.md5s,sha256s=self.sha3_256s,
        )
        return post


    async def _process_media(self,type:str,media:encoding.BaseFile) -> schemas.BaseMedia|None:
        if media is None:
            return None
        
        store_url = self._store_file(type,media)
        self._generate_hashes(media)
        return self._generate_schema(media,store_url)


    def _store_file(self,type:str,media:encoding.BaseFile) -> str:
        ext:str = mimetypes.guess_extension(media.mimetype) # type: ignore
        key = store.put(media.data,prefix=type,suffix=ext)
        return store.url(key)


    def _generate_hashes(self,file:encoding.BaseFile) -> None:
        md5 = hashlib.md5(file.data).hexdigest()
        sha3 = hashlib.sha3_256(file.data).hexdigest()
        self.md5s.append(md5)
        self.sha3_256s.append(sha3)


    def _generate_schema(self,file:encoding.BaseFile,url) -> schemas.BaseMedia:
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
        else:
            raise Exception("Unknown File class")
        
        return schema