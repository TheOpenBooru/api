import typing
from modules import account as _account
from modules.account import Account
from fastapi import HTTPException as _HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")

async def DecodeToken(token:str = Depends(oauth2_scheme)) -> _account.Account:
    try:
        login = _account.decode(token)
    except _account.InvalidToken:
        raise _HTTPException(
            status_code=401,
            detail="Bad Authorization Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return login


def RequirePermission(permission:str):
    if not hasattr(_account.Permissions, permission):
        raise ValueError(f"Invalid Permission: {permission}")
    
    async def wrapper(token:str = Depends(oauth2_scheme)):
        try:
            login = _account.decode(token)
        except _account.InvalidToken:
            raise _HTTPException(
                status_code=401,
                detail="Bad Authorization Token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        perms = dict(login.permissions)
        action_allowed = perms[permission]
        if not action_allowed:
            raise _HTTPException(
                status_code=401,
                detail=f"Requires Permission: {permission}"
            )
    return wrapper