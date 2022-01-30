from modules.database import Tag
from fastapi import APIRouter

router = APIRouter()

@router.get('/all')
def tag_list():
    return Tag.list_all()