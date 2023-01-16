from . import router
from modules import schemas, fastapi, database
from modules.fastapi import PermissionManager, RequireAccount
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@router.get("",
    response_model=schemas.User,
    dependencies=[
        Depends(PermissionManager("canViewProfile")),
        Depends(RequireAccount),
    ],
)
async def get_profile(account: fastapi.GetAccount = Depends()):
    if account.user_id == None or database.User.exists(account.user_id) == False:
        raise HTTPException(status_code=401)
    else:
        user = database.User.get(account.user_id)
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(user),
        )
