from . import oauth2_scheme
from modules import account as _account
from fastapi import HTTPException, Depends


async def DecodeToken(token:str = Depends(oauth2_scheme)) -> _account.Account:
    try:
        login = _account.decode(token)
    except _account.InvalidToken:
        raise HTTPException(
            status_code=401,
            detail="Bad Authorization Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return login
