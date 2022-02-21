from . import router
from modules import jwt,schemas,database
from endpoints.dependencies.auth import parse_token
from fastapi import Response,Depends,status

@router.delete("/post/{id}")
async def delete_post(id:int ,token:jwt.TokenData=Depends(parse_token)):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)
