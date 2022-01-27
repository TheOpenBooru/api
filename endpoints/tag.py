from modules.database import tag
from fastapi import APIRouter

router = APIRouter()

@router.get('/all')
def tag_list():
    return tag.list_all()