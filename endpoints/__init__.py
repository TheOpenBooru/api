from fastapi import APIRouter
router = APIRouter()
from . import post,tag,misc

router.include_router(post.router)
router.include_router(tag.router)
router.include_router(misc.router)