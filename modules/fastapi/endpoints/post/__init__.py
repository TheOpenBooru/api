from fastapi import APIRouter

router = APIRouter(prefix="/post",tags=["Post"])
from . import edit, get, delete, downvote, upvote
router.include_router(downvote.router)
router.include_router(upvote.router)