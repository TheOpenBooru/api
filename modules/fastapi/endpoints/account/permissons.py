from . import router
from modules import schemas, account
from modules.account.permissions import Permissions
from fastapi import Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Union


@router.get("/permissions",
    response_model=schemas.UserPermissions,
)
async def get_permissions(token: Union[str,None] = Header(None, alias="Authorization")):
    if token == None:
        perms = Permissions.from_level("annonymous")
    else:
        user = account.decode(token)
        perms = user.permissions.permissions
    
    return JSONResponse(jsonable_encoder(perms))