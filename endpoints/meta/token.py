from fastapi import Header as _Header, HTTPException as _HTTPException
from modules.account import Account,InvalidToken
from modules import account as _account

async def DecodeToken(Authorization:str = _Header()):
    try:
        type,token = Authorization.split(' ')
    except Exception:
        raise _HTTPException(status_code=401,detail="Missing Authorization Header")
    
    if type != "Bearer":
        raise _HTTPException(status_code=401,detail="Invalid Authorization Header")
    
    try:
        login = _account.decode(token)
    except InvalidToken:
        raise _HTTPException(status_code=400, detail="Invalid token")
    else:
        return login
