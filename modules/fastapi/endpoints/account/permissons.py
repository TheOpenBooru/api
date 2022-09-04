from . import router
from modules import schemas, account
from modules.fastapi import oauth2_scheme
from modules.account.permissions import Permissions
from fastapi import Header, HTTPException
from typing import Union


@router.get("/permissions",
    response_model=schemas.UserPermissions,
)
async def get_permissions(token: Union[str,None] = Header(None, alias="Authorization")):
    if token == None:
        perms = Permissions.from_level("annonymous")
    else:
        token = token[len("Bearer "):]
        try:
            user = account.decode(token)
        except account.InvalidToken:
            raise HTTPException(
                status_code=401,
                detail="Bad Authorization Token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        perms = user.permissions
    
    return perms.permissions