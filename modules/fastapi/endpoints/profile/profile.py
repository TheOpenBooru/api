from . import router
from modules import database, schemas, account,fastapi
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("",
    responses={
        200:{"description":"Profile Data Retrieved Successfully"},
        401:{"description":"Not Logged In"},
    },
    response_model=schemas.User,
)
async def get_profile(account:account.Account = Depends(fastapi.DecodeToken)):
    user = database.User.get(account.id)
    return JSONResponse(jsonable_encoder(user),status_code=200)
