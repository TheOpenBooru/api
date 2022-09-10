from fastapi import APIRouter, Depends
from modules.fastapi import hasPermission

router = APIRouter(
    dependencies=[
        Depends(hasPermission("canVotePosts")),
    ],
    responses={
        404: {"description": "Post Not Found"}
    },
)

from . import add, remove