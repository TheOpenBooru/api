from . import oauth2_scheme
from modules import account, schemas
from fastapi import HTTPException as _HTTPException, Depends

VALID_PERMISSION = set(schemas.UserPermissions().dict().keys())
class RequirePermission:
    action:str
    
    def __init__(self, permission:str):
        if permission not in VALID_PERMISSION:
            raise ValueError(f"Invalid Permission: {permission}")

        self.action = permission

    def __call__(self,token:str = Depends(oauth2_scheme)):
            try:
                login = account.decode(token)
            except account.InvalidToken:
                raise _HTTPException(
                    status_code=401,
                    detail="Bad Authorization Token",
                    headers={"WWW-Authenticate": "Bearer"},
                ) 
            if not login.permissions.hasPermission(self.action):
                raise _HTTPException(
                    status_code=401,
                    detail=f"Requires Permission: {self.action}"
                )