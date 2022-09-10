from . import router
from modules import schemas, account, fastapi
from modules.fastapi import RequirePermission
from modules.database import User
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("",
    response_model=schemas.User,
    dependencies=[
        Depends(RequirePermission("canViewProfile")),
    ],
)
async def get_profile(account: fastapi.DecodeToken = Depends()):
    if account.user_id == None or User.exists(account.user_id) == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        user = User.get(account.user_id)
        payload = jsonable_encoder(user)
        return JSONResponse(
            content=payload,
            status_code=200
        )
