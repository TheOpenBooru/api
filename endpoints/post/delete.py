from . import router
from modules import jwt
from fastapi import Response,Depends,status

@router.delete("/post/{id}")
async def delete_post(id:int):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)
