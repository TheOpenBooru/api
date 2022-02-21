from . import router
from modules import schemas,jwt
from fastapi import Response,status

@router.post("/create")
async def create_post():
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)
