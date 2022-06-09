from . import router
from modules import database, schemas
from endpoints.meta.token import Account, DecodeToken
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


responses = {
    200:{"description":"Profile Data Retrieved Successfully"},
    400:{"description":"Not Logged In"},
}

@router.get("/profile",
    response_model=schemas.User,
    responses=responses,
) # type: ignore
async def login(account:Account = Depends(DecodeToken)):
    user = database.User.get(account.id)
    return JSONResponse(jsonable_encoder(user),status_code=200)
