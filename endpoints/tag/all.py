from . import router
from modules import schemas,database
from fastapi import Response, responses, status

@router.get('/all',response_model=list[schemas.Tag])
def get_all_tags():
    return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    tags = database.Tag.all()
    return tags