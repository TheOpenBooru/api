from . import router
from modules import auth,jwt
from fastapi import Response,status


@router.post("/login")
async def login(username:str,password:str):
    authorised = auth.login(username,password)
    if not authorised:
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
