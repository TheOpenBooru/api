from . import router
from modules import schemas, account
from fastapi import Response, Body


@router.post("/register",
    responses={
        200:{"description":"Successfully Signed up"},
        400:{"description":"Password does not meet requirements"},
        409:{"description":"Username already exists"},
    },
)
async def register(username: str = Body(), password: str = Body()):
    try:
        account.register(username, password)
    except account.AccountAlreadyExists:
        return Response("User already exists",409)
    except account.InvalidPassword:
        return Response("Password Does not meet requirements",400)
    else:
        token = account.login(username, password)
        return token
