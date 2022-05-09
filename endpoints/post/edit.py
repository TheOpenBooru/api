from . import router
from modules import schemas
from modules.database import Post
from fastapi import Response,status

responses = {
    404:{"description":"The Post Could Not Be Found"},
    400:{"description":"Not Implemented"},
}

@router.patch('/post/{id}',
    responses=responses, # type: ignore
)
async def edit_post(id:int,post_update:schemas.Post_Edit):
    if not Post.exists(id):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
