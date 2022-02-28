from fastapi import APIRouter
router = APIRouter()
from . import image,post,status

router.include_router(image.router)
router.include_router(post.router)