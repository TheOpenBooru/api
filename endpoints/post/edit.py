from . import router
from modules import schemas,database,jwt
from endpoints.dependencies.auth import parse_token
from fastapi import Response,Depends,status

@router.patch('/post', tags=['User'])
async def edit_post(id:int,new_post_version:schemas.Post,token:jwt.TokenData=Depends(parse_token)):
    if token.level == "ADMIN":
        database.Post.update(id,new_post_version)
        return Response(status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED,content="Not High Enough Level")
