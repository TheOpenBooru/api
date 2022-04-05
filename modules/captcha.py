from modules import settings
import requests
import logging

DEFAULT_SECRET = settings.HCAPTCHA_SECRET

def get_sitekey() -> str:
    return settings.HCAPTCHA_SITEKEY

def verify(captcha_response:str,secret:str = DEFAULT_SECRET) -> bool:
    r = requests.post(
        "https://hcaptcha.com/siteverify",
        data={
            "secret": secret,
            "response": captcha_response
        }
    )
    if not r.ok:
        logging.error(f"Error while verifying captcha: {r.text}")
        return False
    else:
        json = r.json()
        return json['success']
