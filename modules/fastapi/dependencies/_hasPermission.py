from . import oauth2_scheme
from modules import account, schemas
from modules.fastapi.dependencies import DecodeToken
from modules.account.permissions import Permissions
from fastapi import HTTPException, Depends, status, Header
from typing import Union

VALID_PERMISSIONS = set(schemas.UserPermissions().dict().keys())
class hasPermission:
    action:str
    
    def __init__(self, permission:str):
        if permission not in VALID_PERMISSIONS:
            raise ValueError(f"Invalid Permission: {permission}")

        self.action = permission

    def __call__(self, account: DecodeToken = Depends()):
        perms = account.permissions
        
        if not perms.hasPermission(self.action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires Permission: {self.action}",
            )
