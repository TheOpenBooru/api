import os
import logging
import requests

SITEKEY = os.getenv("HCAPTCHA_SITE_KEY")
_SECRET = os.getenv("HCAPTCHA_SECRET")

def verify(response:str) -> bool:
    r = requests.post("https://hcaptcha.com/siteverify", data={
        "secret": _SECRET,
        "response": response
    })
    if r.ok:
        JSON = r.json()
        return JSON['success']
    else:
        logging.warning("Failed to verify captcha:",r.text)
        return False
