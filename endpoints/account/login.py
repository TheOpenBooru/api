from . import router
from modules import account
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response, Depends


@router.post("/login",
    response_model=str,
    responses={
        200:{
            "description":"Successfully Signed in and Provided a Token",
            "content": {"text/plain":{}}
        },
        404:{"description":"Invalid Username or Password"},
        406:{"description":"User's Password Was Reset"},
    }
)
async def login(oauth:OAuth2PasswordRequestForm = Depends()):
    try:
        token = account.login(oauth.username,oauth.password)
    except account.LoginFailure:
        return Response("Invalid Username or Password",401)
    except account.PasswordWasReset:
        return Response("Please reset your password",406)
    else:
        return Response(token,200)

