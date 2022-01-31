from modules import settings
import os
import logging
import requests

def sitekey() -> str:
    return settings.get('config.hcaptcha.sitekey')

def verify(response:str) -> bool:
    r = requests.post("https://hcaptcha.com/siteverify", data={
        "secret": settings.get('config.hcaptcha.secret'),
        "response": response
    })
    if r.ok:
        JSON = r.json()
        return JSON['success']
    else:
        logging.warning("Failed to verify captcha:",r.text)
        return False
