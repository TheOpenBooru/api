from . import oauth2_scheme
import zlib
from typing import Optional, Union
from modules import account
from modules.account import Permissions, Account
from fastapi import HTTPException, Depends, Request


class DecodeToken:
    id: int
    user_id: Optional[int]
    username: str
    permissions: Permissions
    
    def __init__(self, request: Request, token:Union[str, None] = Depends(oauth2_scheme)):
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