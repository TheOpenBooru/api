from . import router
from modules import auth, schemas, jwt
from modules.database import User
from fastapi import Response, status, Body


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
    query = schemas.User_Query(username=username)
    users = User.search(query)
    if len(users) == 0:
        return Response(
            "Invalid Username or Password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    else:
        user = users[0]
        if not auth.exists(username):
            return Response(
                "User's Password was reset. Please contact the administrator",
                status_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        else:
            authorised = auth.login(username,password)
            if not authorised:
                return Response(
                    "Invalid Username or Password",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            else:
                token = jwt.create({
                        "username":user.username,
                        "level":user.level,
                    }
                )
                return Response(
                    token,
                    status_code=status.HTTP_200_OK,
                )
