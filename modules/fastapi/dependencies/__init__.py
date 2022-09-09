from fastapi.security import OAuth2PasswordBearer as _OAuth2PasswordBearer
oauth2_scheme = _OAuth2PasswordBearer(tokenUrl="/account/login", auto_error=False)

from modules.account import Account
from ._decodeToken import DecodeToken
from ._captcha import RequireCaptcha
from ._permission import RequirePermission
from ._ratelimit import RateLimit
