from . import router
from modules import account, schemas, fastapi
from pydantic import BaseModel
from fastapi import Body, Depends
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder


@router.post("/register",
    operation_id="register",
    response_model=schemas.Token,
    responses={
        400:{"description":"Password does not meet requirements"},
        409:{"description":"Username already exists"},
    },
    dependencies=[
        Depends(fastapi.RequirePermission("canRegister")),
    ],
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
        return schemas.Token(
            access_token=token,
            token_type="bearer"
        )
