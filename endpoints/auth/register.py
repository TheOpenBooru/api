from . import router
from modules import auth
from fastapi import Response,status


@router.post("/register")
async def register(username: str, password: str):
    try:
        auth.register(username,password)
    except KeyError:
        return Response("User already exists",status_code=status.HTTP_409_CONFLICT)
    except ValueError:
        return Response("Bad Password",status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status_code=status.HTTP_201_CREATED)
