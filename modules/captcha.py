import os
import logging
import requests

def sitekey():
    return str(os.getenv("HCAPTCHA_SITE_KEY"))

def verify(response:str) -> bool:
    r = requests.post("https://hcaptcha.com/siteverify", data={
        "secret": os.getenv("HCAPTCHA_SECRET"),
        "response": response
    })
    if r.ok:
        JSON = r.json()
        return JSON['success']
    else:
        logging.warning("Failed to verify captcha:",r.text)
        return False
