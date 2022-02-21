from . import router
from modules import schemas
from fastapi import Response,status

@router.patch('/post/{id}')
async def edit_post(id:int,new_post_version:schemas.Post):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)
