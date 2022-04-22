from . import router
from modules import schemas,database
from fastapi import Response,status

@router.patch('/post/{id}')
async def edit_post(id:int,new_post_version:schemas.Post):
    return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    if database.Post.get(id=id):
        database.Post.update(id,new_post_version)
        return Response(status_code=status.HTTP_205_RESET_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
