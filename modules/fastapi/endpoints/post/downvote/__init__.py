from fastapi import APIRouter, Depends
from modules.fastapi import hasPermission

router = APIRouter(
    responses={
        404: {"description": "Post Not Found"}
    },
)

from . import add, remove