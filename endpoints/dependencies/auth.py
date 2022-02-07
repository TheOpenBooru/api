from modules.auth import jwt
from fastapi import Header

async def parse_token(Authorization: str = Header(...)) -> jwt.TokenData | None:
    try:
        tokenData = jwt.decode(Authorization)
    except jwt.BadTokenError:
        return None
    else:
        return tokenData
