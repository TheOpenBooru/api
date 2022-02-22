import io
from . import router
from modules import image,database,store,schemas,settings
from modules.schemas import Post
import time
import hashlib
from fastapi import Response,status,UploadFile 

@router.post("/create")
async def create_post(image_file:UploadFile):
    md5s = []
    sha3_256s = []
    def process_file_hashes(data:bytes):
        md5 = hashlib.md5(data).hexdigest()
        md5s.append(md5)
        sha3 = hashlib.sha3_256(data).hexdigest()
        sha3_256s.append(sha3)
    
    # image_data:bytes = await image_file.read() # type:ignore
    # process_file_hashes(image_data)
    
    full_image = image.file_to_image(image_file.file)
    full = await process_image(full_image)
    process_file_hashes(full_image.data)
    
    preview_image = image.generatePreview(full_image)
    preview = await process_image(preview_image)
    process_file_hashes(preview_image.data)
    
    thumbnail_image = image.generateThumbnail(full_image)
    thumbnail = await process_image(thumbnail_image)
    process_file_hashes(thumbnail_image.data)

    postID = database.Post.get_unused_id()
    post = Post(
        id=postID,creator=1,
        sound=False,type='image',
        full=full,preview=preview,thumbnail=thumbnail,
        md5s=md5s,sha256s=sha3_256s,
    )
    try:
        database.Post.create(post)
        return Response(status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response(str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

async def process_image(img:image.Image) -> schemas.Image:
    key = store.put(img.data,suffix=".webp")
    width,height = img.resolution.to_tuple()
    image_data = schemas.Image(
        url=store.url(key),
        width=width,height=height,
        mimetype='image/webp'
    )
    return image_data
