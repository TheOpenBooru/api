from . import router
from modules import jwt,schemas,database
from endpoints.dependencies.auth import parse_token
from fastapi import Response,Depends,status

@router.delete("/post/{id}", tags=['Moderator'])
async def delete_post(id:int ,token:jwt.TokenData=Depends(parse_token)):
    if token.level == "ADMIN":
        database.Post.delete(id)
        return Response(status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED,content="Not High Enough Level")
