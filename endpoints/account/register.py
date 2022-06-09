from . import router
from modules import auth, schemas
from modules.database import User
from fastapi import Response, status, Body


responses = {
    201:{"description":"Successfully Signed up"},
    400:{"description":"Password does not meet requirements"},
    409:{"description":"Username already exists"},
}

@router.post("/register",responses=responses) # type: ignore
async def register(username: str = Body(), password: str = Body()):
    query = schemas.User_Query(username=username)
    users = User.search(query)
    if len(users) > 0:
        return Response(
            status_code=status.HTTP_409_CONFLICT,
            content="User already exists",
        )
    elif not auth.is_password_valid(password):
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Password Does not meet requirements",
        )
    else:
        user = schemas.User(
            id=User.get_unique_id(),
            username=username,
        )
        auth.register(username,password)
        User.create(user)
        return Response(
            status_code=status.HTTP_201_CREATED
        )
