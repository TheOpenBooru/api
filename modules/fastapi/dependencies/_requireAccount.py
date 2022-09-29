from . import oauth2_scheme, DecodeToken
from fastapi import HTTPException, Depends


async def RequireAccount(account:DecodeToken = Depends()):
    if account.user_id == None:
        raise HTTPException(status_code=401)
