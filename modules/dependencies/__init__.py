from fastapi.security import OAuth2PasswordBearer as _OAuth2PasswordBearer
oauth2_scheme = _OAuth2PasswordBearer(tokenUrl="/account/login")

from modules.account import Account
from ._decodeToken import DecodeToken
from ._permission import RequirePermission
