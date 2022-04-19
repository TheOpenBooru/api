from . import router
from modules import schemas,posts
from fastapi import Response,status,UploadFile 
import hashlib
import mimetypes
mimetypes.add_type('image/webp','.webp')

@router.post("/create",response_model=schemas.Post,status_code=status.HTTP_201_CREATED)
async def create_post(image_file:UploadFile):
    data = await image_file.read()
    filename = image_file.filename
    try:
        post = await posts.create(data,filename) # type: ignore
    except Exception as e:
        return Response("General Failure",status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return post