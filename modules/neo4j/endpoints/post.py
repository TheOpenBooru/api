from typing import List
from modules.neo4j import Post
from fastapi import Response, Query
from fastapi.responses import JSONResponse
import json


def posts_get(post_ids: List[int] = Query(None)):
    return {"q": post_ids}

def posts_get(post_ids: List[int]  = Query(None)):
    if not post_ids:
        return Response(status_code=400)
    
    posts = []
    for id in post_ids:
        post = Post.get(id=id)
        if post:
            posts.append(post)
    return JSONResponse(
            content=posts,
            media_type='application/json',
            headers={'Access-Control-Allow-Origin':'*'}
            )

def post_search(tags:List[str] = Query(None),sort:str = None,limit:int = None):
    kwargs = {}
    if tags: kwargs['tags'] = tags
    if sort: kwargs['sort'] = sort
    if limit: kwargs['limit'] = limit
    posts = Post.search(**kwargs)
    
    return JSONResponse(
            content=posts,
            media_type='application/json',
            headers={
                'Cache-Control': 'public max-age=31536000',
                'Access-Control-Allow-Origin':'*'
            })