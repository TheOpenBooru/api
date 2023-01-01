from . import oauth2_scheme
from openbooru.modules import account, settings, captcha
from fastapi import HTTPException, Query, status


if settings.HCAPTCHA_ENABLED and not settings.DISABLE_PERMISSIONS:
    async def RequireCaptcha(captcha_response: str = Query(...,alias="h-captcha-response")):
        if not captcha.verify(captcha_response):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid Captcha Response")
else:
    async def RequireCaptcha(captcha_response: str = Query(default="", alias="h-captcha-response")):
        pass
