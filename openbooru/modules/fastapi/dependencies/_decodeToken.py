from . import oauth2_scheme
from openbooru.modules import account
from openbooru.modules.account import Permissions, Account
import zlib
from fastapi import HTTPException, Depends, Request


class GetAccount:
    id: int
    user_id: int|None
    username: str
    permissions: Permissions
    
    def __init__(self, request: Request, token: str|None = Depends(oauth2_scheme)):
        if token == None:
            self._generate_annonomous_account(request)
        else:
            self._generate_account(token)


    def _generate_annonomous_account(self, request:Request):
        ip = request.client.host
        self.id = zlib.crc32(ip.encode())
        self.user_id = None
        self.username = "Annonymous"
        self.permissions = Permissions.from_level("annonymous")

    
    def _generate_account(self, token:str):
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        
        try:
            login = account.decode(token)
        except account.InvalidToken:
            raise HTTPException(
                status_code=401,
                detail="Bad Authorization Token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            self.id = login.id
            self.user_id = login.id
            self.username = login.username
            self.permissions = login.permissions