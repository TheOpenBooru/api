from . import router
from openbooru.modules import account, schemas, fastapi, users
from pydantic import BaseModel
from fastapi import Body, Depends, HTTPException
from fastapi.responses import PlainTextResponse


@router.post("/register",
    response_model=schemas.Token,
    responses={
        400:{
            "description":"Creation Failure with Error Message",
            "content": {"text/plain": {}},
        },
    },
    dependencies=[
        Depends(fastapi.PermissionManager("canRegister")),
    ],
)
async def register(username: str = Body(), password: str = Body()):
    try:
        users.create(username, password)
    except users.UsernameAlreadyExists:
        raise HTTPException(400, "A User with that name already exists")
    except users.InvalidPassword:
        raise HTTPException(400, "Password Does not meet requirements")
    except users.InvalidUsername:
        raise HTTPException(400, "Username Does not meet requirements")
    else:
        token = account.login(username, password)
        return schemas.Token(
            access_token=token,
            token_type="bearer"
        )
