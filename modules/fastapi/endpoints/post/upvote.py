from . import router
from modules import database, fastapi, users
from modules.fastapi.dependencies import DecodeToken, Account
from pydantic import BaseModel
from enum import Enum
from typing import Union, Literal
from fastapi import Response, Depends



@router.post("/{id}/upvote",
    responses={
        202:{"description":"Success"},
        404:{"description":"Post Not Found"},
    },
    dependencies=[Depends(fastapi.RequirePermission("canVotePosts"))],
)
async def post_post_upvote(id:int, account: Account = Depends(DecodeToken)):
    if not database.Post.exists(id):
        return Response("Post Not Found", status_code=404)
    
    user = database.User.get(account.id)
    if id in user.downvotes:
        database.User.add_upvote(user.id,id)
        database.Post.add_upvote(id)
        database.Post.remove_downvote(id)
        database.User.remove_downvote(user.id,id)
    elif id in user.upvotes:
        database.User.remove_upvote(user.id,id)
        database.Post.remove_upvote(id)
    else:
        database.User.add_upvote(user.id,id)
        database.Post.add_upvote(id)
    
    return Response("Success", status_code=200)
