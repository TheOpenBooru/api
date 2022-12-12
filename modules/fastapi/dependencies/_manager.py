from . import oauth2_scheme
from modules import schemas, captcha, ratelimit, settings
from modules.fastapi.dependencies import DecodeToken
from modules.account.permissions import Permissions
from fastapi import HTTPException, Depends, status, Header, Request

VALID_PERMISSION = set(schemas.UserPermissions().dict().keys())
class PermissionManager:
    action:str

    def __init__(self, permission:str):
        if permission not in VALID_PERMISSION:
            raise ValueError(f"Invalid Permission: {permission}")
        
        self.action = permission


    def __call__(self, request: Request, account:DecodeToken = Depends()):
        if settings.DISABLE_PERMISSIONS:
            return
        
        self.check_permission(account.permissions)
        self.check_captcha(request, account.permissions)
        self.check_ratelimit(account)


    def check_permission(self, permissions: Permissions):
        if not permissions.hasPermission(self.action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires Permission: {self.action}",
            )


    def check_captcha(self, request: Request, permissions: Permissions):
        if not settings.HCAPTCHA_ENABLE:
            return
        
        if not permissions.isCaptchaRequired(self.action):
            return
        
        response = request.query_params.get("h-captcha-response", default=None)
        if response == None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"H-Captcha Required",
            )
        
        if captcha.verify(response) == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bad H-Captcha Response",
            )

    
    def check_ratelimit(self, account: DecodeToken):
        ratelimtString = account.permissions.getRateLimit(self.action)
        if ratelimtString:
            try:
                id = f"{self.action}-{account.id}"
                ratelimit.ratelimit(id, ratelimtString)
            except ratelimit.RateLimitException as e:
                raise HTTPException(
                    status.HTTP_429_TOO_MANY_REQUESTS,
                    headers={"Retry-After": str(e.until)}
                    )
