from fastapi import APIRouter

router = APIRouter(
    prefix="/post",
    tags=["Post"],
    responses={
        404: {"description": "Post Not Found"}
    }
)

from . import edit, get, delete, votes