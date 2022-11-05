from fastapi import APIRouter

router = APIRouter()
from . import media, status, index
from . import account, profile, posts, post, tag, subscription

router.include_router(subscription.router)
router.include_router(account.router)
router.include_router(profile.router)
router.include_router(posts.router)
router.include_router(post.router)
router.include_router(tag.router)
