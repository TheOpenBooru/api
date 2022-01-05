from typing import List
from . import Post,Tag
from fastapi import Response, Query
from fastapi.responses import JSONResponse
import json


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
    posts = Post.search(tags=['test'])
    
    return JSONResponse(
            content=posts,
            media_type='application/json',
            headers={
                'Cache-Control': 'public max-age=31536000',
                'Access-Control-Allow-Origin':'*'
            })


def tag_get(tags:List[str] = Query(None)):
    tagObjects = {}
    return JSONResponse(
        content=tagObjects,
        media_type='application/json',
        headers={
            'Cache-Control': 'public max-age=31536000',
            'Access-Control-Allow-Origin':'*'
        })

def tag_list():
    return JSONResponse(
        content=Tag.list(),
        media_type='application/json',
        headers={
            'Cache-Control': 'public max-age=31536000',
            'Access-Control-Allow-Origin':'*'
        })