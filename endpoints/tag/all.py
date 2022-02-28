from . import router
from modules import schemas,database
from fastapi import responses, status

@router.get('/all',response_model=list[schemas.Tag])
def get_all_tags():
    tags = database.Tag.all()
    return tags