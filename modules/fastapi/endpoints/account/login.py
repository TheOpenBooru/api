from . import router
from modules import account
from modules.fastapi.dependencies import RateLimit
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder


@router.post("/login",
    operation_id="login",
    response_model=str,
    responses={
        200:{"description":"Successfully Signed in and Provided a Token"},
        401:{"description":"Invalid Username or Password"},
        406:{"description":"User's Password Was Reset"},
    },
    dependencies=[Depends(RateLimit("5/minute"))]
)
async def login(oauth:OAuth2PasswordRequestForm = Depends()):
    try:
        token = account.login(oauth.username,oauth.password)
    except (account.LoginFailure, account.AccountDoesntExists):
        return PlainTextResponse("Invalid Username or Password",401)
    except account.PasswordWasReset:
        return PlainTextResponse("Please reset your password",406)
    else:
        data = {
            "access_token": token,
            "token_type": "bearer"
        }
        json = jsonable_encoder(data)
        return JSONResponse(json)
