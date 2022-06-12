from . import router
from modules import schemas
from modules.database import Post
from fastapi import Response,status


@router.patch('/post/{id}',
    responses={
        404:{"description":"The Post Could Not Be Found"},
        400:{"description":"Not Implemented"},
    }, # type: ignore
)
async def edit_post(id:int,post_update:schemas.Post_Edit):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)
