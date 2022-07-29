from . import oauth2_scheme
from modules import account, settings, captcha
from fastapi import HTTPException, Query, status


if settings.HCAPTCHA_ENABLE:
    async def RequireCaptcha(captcha_response:str = Query(...,alias="h-captcha-response")): # type: ignore
        if captcha.verify(captcha_response) == False:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid Captcha Response")
else:
    async def RequireCaptcha():
        pass
