from . import router
from modules import schemas
from modules.database import Post
from fastapi import Response,status

@router.patch('/post/{id}')
async def edit_post(id:int,post_update:schemas.Post_Edit):
    if not Post.exists(id):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
