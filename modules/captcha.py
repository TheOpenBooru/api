from modules import settings
import requests
import logging

def sitekey() -> str:
    return settings.get('config.hcaptcha.sitekey')

def verify(captcha_response:str) -> bool:
    r = requests.post(
        "https://hcaptcha.com/siteverify",
        data={
            "secret": settings.get('config.hcaptcha.secret'),
            "response": captcha_response
        }
    )
    if not r.ok:
        logging.error(f"Error while verifying captcha: {r.text}")
        return False
    else:
        json = r.json()
        return json['success']
