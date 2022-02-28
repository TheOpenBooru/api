from fastapi import APIRouter
router = APIRouter()
from . import image,post,tag,status

router.include_router(image.router)
router.include_router(post.router)
router.include_router(tag.router)