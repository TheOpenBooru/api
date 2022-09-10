from . import router
from modules import account, fastapi, schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder


@router.post("/login",
    operation_id="login",
    response_model=schemas.Token,
    responses={
        401:{"description":"Invalid Username or Password"},
        406:{"description":"User's Password Was Reset"},
    },
    dependencies=[
        Depends(fastapi.RequirePermission("canLogin")),
    ]
)
async def login(oauth:OAuth2PasswordRequestForm = Depends()):
    try:
        token = account.login(oauth.username,oauth.password)
    except (account.LoginFailure, account.AccountDoesntExists):
        return PlainTextResponse("Invalid Username or Password",401)
    except account.PasswordWasReset:
        return PlainTextResponse("Please reset your password",406)
    else:
        return schemas.Token(
            access_token=token,
            token_type="bearer"
        )
