from . import router
from modules import schemas,database,jwt
from endpoints.dependencies.auth import parse_token
from fastapi import Response,Depends,status

@router.patch('/post/{id}')
async def edit_post(id:int,new_post_version:schemas.Post,token:jwt.TokenData=Depends(parse_token)):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)
