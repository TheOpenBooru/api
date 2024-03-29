from . import router
from modules import database, posts
from modules.fastapi.dependencies import GetAccount, PermissionManager, RequireAccount
from fastapi import Response, Depends, HTTPException, APIRouter


votes_router = APIRouter(
    dependencies=[
        Depends(PermissionManager("canVotePosts")),
        Depends(RequireAccount),
    ],
    responses={
        404: {"description": "Post Not Found"}
    }
)
router.include_router(votes_router)

def assert_post_exists(post_id:int):
    if not database.Post.exists(id=post_id):
        raise HTTPException(404, "Post Not Found")


@votes_router.post("/{id}/upvote/add")
async def add_upvote(id:int, account: GetAccount = Depends()):
    assert_post_exists(id)
    posts.add_upvote(id, account.id)


@votes_router.post("/{id}/upvote/remove")
async def remove_upvote(id:int, account: GetAccount = Depends()):
    assert_post_exists(id)
    posts.remove_upvote(id, account.id)

@votes_router.post("/{id}/downvote/add")
async def add_downvote(id:int, account: GetAccount = Depends()):
    assert_post_exists(id)
    posts.add_downvote(id, account.id)


@votes_router.post("/{id}/downvote/remove")
async def remove_downvote(id:int, account: GetAccount = Depends()):
    assert_post_exists(id)
    posts.remove_downvote(id, account.id)
