from fastapi import APIRouter
router = APIRouter()
from . import account,post,misc

router.include_router(account.router)
router.include_router(post.router)
router.include_router(misc.router)
