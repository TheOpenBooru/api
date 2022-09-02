from . import router
from modules import schemas, account,fastapi
from modules.database import User
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("",
    response_model=schemas.User,
)
async def get_profile(account:account.Account = Depends(fastapi.DecodeToken)):
    if not User.exists(account.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        user = User.get(account.id)
        payload = jsonable_encoder(user)
        return JSONResponse(
            content=payload,
            status_code=200
        )
