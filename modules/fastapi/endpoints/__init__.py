from fastapi import APIRouter

router = APIRouter()
from . import account, profile, posts, post, tag, media, status, subscription

router.include_router(subscription.router)
router.include_router(account.router)
router.include_router(profile.router)
router.include_router(posts.router)
router.include_router(post.router)
router.include_router(tag.router)
