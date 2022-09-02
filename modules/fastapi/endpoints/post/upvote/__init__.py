from fastapi import APIRouter, Depends
from modules.fastapi import RequirePermission

router = APIRouter(
    dependencies=[
        Depends(RequirePermission("canVotePosts")),
    ],
    responses={
        404: {"description": "Post Not Found"}
    },
)

from . import add, remove