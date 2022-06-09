from fastapi import Query as _Query, HTTPException as _HTTPException
from modules.account import Account
from modules import account as _account

async def DecodeToken(token:str = _Query(None)) -> Account:
    try:
        login = _account.decode(token)
    except:
        raise _HTTPException(status_code=400, detail="Invalid token")
    else:
        return login
