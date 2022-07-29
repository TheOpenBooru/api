from . import router
from modules import schemas
from modules.fastapi.dependencies import RateLimit
from modules.database import Post
from fastapi import Response, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/{id}",
    response_model=schemas.Post,
    status_code=status.HTTP_200_OK,
    responses={
        200:{"description":"Successfully Retrieved Post"},
        404:{"description":"The Post Could Not Be Found"},
    },
    dependencies=[
        Depends(RateLimit("2/second")),
    ]
)
async def get_post(id:int):
    CACHE_HEADER = {"Cache-Control": "max-age=60, public"}
    if not Post.exists(id):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        post = Post.get(id)
        return JSONResponse(
            content=jsonable_encoder(post),
            headers=CACHE_HEADER,
            status_code=status.HTTP_200_OK,
        )
