from . import router
from modules import auth, jwt, schemas, email
from modules.database import User
from fastapi import Response,status


responses = {
    202:{
        "description":"Successfully Signed in and Provided a Token",
        "content": {
            "text/plain":{
                "example":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.m5V22b06bOUSSzrDzcGusUKjnvTZMHpIGI__nY3t328"
            }
        }
    },
    404:{
        "description":"Invalid Username or Password"
    },
    406:{
        "description":"User's Password was reset. Please contact the administrator"
    },
}

@router.post("/login",response_model=str,responses=responses) # type: ignore
async def login(username:str,password:str):
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
                token = jwt.create(
                    id=user.id,
                    additional_data={
                        "username":user.username,
                        "level":user.level,
                    }
                )
                return Response(
                    token,
                    status_code=status.HTTP_202_ACCEPTED,
                )
