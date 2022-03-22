from . import router
from modules import schemas,search
from fastapi.responses import JSONResponse

@router.get("/search", response_model=list[schemas.Post])
async def search_posts(query:str=""):
    CACHE_HEADER = {"Cache-Control": "max-age=60, public"}
    search_settings = search.parseBSLs(query)
    posts = search.searchPosts(search_settings)
    return JSONResponse(content=posts, headers=CACHE_HEADER)
