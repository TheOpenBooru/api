from . import router
from modules import schemas,search
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

@router.get("/search", response_model=list[schemas.Post])
async def search_posts(query:str=""):
    CACHE_HEADER = {"Cache-Control": "max-age=60, public"}
    search_settings = search.parseBSLs(query)
    posts = search.searchPosts(search_settings)
    json = jsonable_encoder(posts)
    return JSONResponse(
        content=json,
        headers=CACHE_HEADER,
    )
