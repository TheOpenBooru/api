from . import oauth2_scheme, GetAccount
from fastapi import HTTPException, Depends


async def RequireAccount(account:GetAccount = Depends()):
    if account.user_id == None:
        raise HTTPException(status_code=401)
