from modules.auth import jwt
from fastapi import Header,APIRouter,Request, Response,status

router = APIRouter()

async def parse_token(Authorization: str = Header(...)) -> jwt.TokenData:
    return jwt.decode(Authorization)


async def bad_token_exception_handler(request: Request, exc: jwt.BadTokenError):
    return Response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content="No or Bad Authorization Header")
