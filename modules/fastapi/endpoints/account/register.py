from . import router
from modules import account
from modules.fastapi.dependencies import RateLimit, RequireCaptcha
from pydantic import BaseModel
from fastapi import Body, Depends
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder


@router.post("/register",
    operation_id="register",
    responses={
        200:{"description":"Successfully Signed up"},
        400:{"description":"Password does not meet requirements"},
        409:{"description":"Username already exists"},
    },
    dependencies=[
        Depends(RequireCaptcha),
        Depends(RateLimit("10/minute")),
    ]
)
async def register(username: str = Body(), password: str = Body()):
    try:
        account.register(username, password)
    except account.AccountAlreadyExists:
        return PlainTextResponse("User already exists",409)
    except account.InvalidPassword:
        return PlainTextResponse("Password Does not meet requirements",400)
    else:
        token = account.login(username, password)
        data = {
            "token_type": "bearer",
            "access_token": token,
        }
        json = jsonable_encoder(data)
        return JSONResponse(json)
