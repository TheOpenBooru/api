from . import router
from modules import schemas, posts
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/search",
    response_model=list[schemas.Post],
    status_code=200,
    responses={
        200:{"description":"Successfully Retrieved"},
    },
)
async def search_posts(query: schemas.Post_Query = Depends()):
    searched_posts = await posts.search(query)
    return JSONResponse(
        content=jsonable_encoder(searched_posts),
        headers={"Cache-Control": "max-age=60, public"},
    )
