from . import router
from modules import schemas
from fastapi import Response,status

@router.get('/all',response_model=list[schemas.Tag])
def list_tags():
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)