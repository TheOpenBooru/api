from . import router
from modules import auth,jwt,captcha
from fastapi import Depends,HTTPException,Response,status
import asyncio


@router.post("/login")
async def login(username:str,password:str):
    logged_in = auth.login(username,password)
    if not logged_in:
        return Response(
            "Invalid username or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    else:
        token = jwt.create(0,{"username":username})
        return Response(
            token,
            status_code=status.HTTP_202_ACCEPTED,
        )
