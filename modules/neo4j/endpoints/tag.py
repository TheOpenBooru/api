from typing import List
from starlette.responses import JSONResponse
from modules.auth import _crypto
from modules.neo4j import Tag
from fastapi import FastAPI, Response,Query

def tag_get(tags:List[str] = Query(None)):
    
    if tags is None:
        return Response('no tags provided',status_code=400)
    tagObjects = [Tag.get(name=tag) for tag in tags]
    
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