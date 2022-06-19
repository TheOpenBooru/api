from . import oauth2_scheme
from modules import account as _account
from modules.account import UserPermissions as _UserPermissions
from fastapi import HTTPException as _HTTPException, Depends

ALL_PERMS = set(_UserPermissions().dict().keys())
class RequirePermission:
    permission:str
    
    def __init__(self, permission:str):
        if permission not in ALL_PERMS:
            raise ValueError(f"Invalid Permission: {permission}")
        self.permission = permission

    def __call__(self,token:str = Depends(oauth2_scheme)):
            try:
                login = _account.decode(token)
            except _account.InvalidToken:
                raise _HTTPException(
                    status_code=401,
                    detail="Bad Authorization Token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            perms = dict(login.permissions)
            action_allowed = perms[self.permission]
            if not action_allowed:
                raise _HTTPException(
                    status_code=401,
                    detail=f"Requires Permission: {self.permission}"
                )
    