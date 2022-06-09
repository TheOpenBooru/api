from . import router
from modules import account
from fastapi import Response, Body


responses = {
    200:{
        "description":"Successfully Signed in and Provided a Token",
        "content": {"text/plain":{}}
    },
    404:{"description":"Invalid Username or Password"},
    406:{"description":"User's Password Was Reset"},
}

@router.post("/login",response_model=str,responses=responses) # type: ignore
async def login(username:str = Body(),password:str = Body()):
    try:
        token = account.login(username,password)
    except account.LoginFailure:
        return Response("Invalid Username or Password",401)
    except account.PasswordWasReset:
        return Response("Please reset your password",406)
    else:
        return Response(token,200)

