from modules import database
from fastapi import APIRouter

from modules import schemas

router = APIRouter()

@router.get('/all',response_model=list[schemas.Tag],tags=["Unprivileged"])
def list_tags():
    ...

@router.get('/get',response_model=schemas.Tag,tags=["Unprivileged"])
def get_tag(name:str):
    ...