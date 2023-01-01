from openbooru.modules import settings
import requests
import logging


def get_sitekey() -> str:
    return settings.HCAPTCHA_SITEKEY

def verify(captcha_response:str, alternate_secret:str|None = None) -> bool:
    secret = alternate_secret or settings.HCAPTCHA_SECRET
    try:
        r = requests.post(
            "https://hcaptcha.com/siteverify",
            data={
                "secret": secret,
                "response": captcha_response
            },
            timeout=5
        )
    except Exception as e:
        logging.warning("Could not connect to hcaptcha")
        raise e
    else:
        json = r.json()
        return json['success']
