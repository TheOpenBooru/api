from . import router
from modules import schemas,search

@router.get("/search", response_model=list[schemas.Post])
async def search_posts(query:str=""):
    search_settings = search.parseBSLs(query)
    posts = search.searchPosts(search_settings)
    return posts
