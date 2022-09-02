from . import oauth2_scheme
from modules import account, schemas
from modules.account.permissions import Permissions
from fastapi import HTTPException as _HTTPException, Depends, status, Header

VALID_PERMISSION = set(schemas.UserPermissions().dict().keys())
class RequirePermission:
    action:str
    
    def __init__(self, permission:str):
        if permission not in VALID_PERMISSION:
            raise ValueError(f"Invalid Permission: {permission}")

        self.action = permission

    def __call__(self,token:str|None = Header(default=None, alias="Authorization")):
        try:
            login = account.decode(token)
        except account.InvalidToken:
            perms = Permissions.from_level("annonymous")
        else:
            perms = login.permissions
        
        
        if not perms.hasPermission(self.action):
            raise _HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires Permission: {self.action}",
            )
