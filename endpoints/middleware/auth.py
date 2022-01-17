from .. import app
from fastapi import Request

class AuthException(Exception):
    def __init__(self, hasToken: bool):
        self.hasToken = hasToken

@app.exception_handler(AuthException)    
async def unicorn_exception_handler(request: Request, err: AuthException):
    if err.hasToken:
        return {"message": "Your token is invalid"}
    else:
        return {"message": "Your not authenticated"}


