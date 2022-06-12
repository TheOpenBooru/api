from . import router
from .._token import Account, DecodeToken
from modules import database, schemas
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("/",
    responses={
        200:{"description":"Profile Data Retrieved Successfully"},
        400:{"description":"Not Logged In"},
    },
    response_model=schemas.User
)
async def get_profile(account:Account = Depends(DecodeToken)):
    user = database.User.get(account.id)
    return JSONResponse(jsonable_encoder(user),status_code=200)
