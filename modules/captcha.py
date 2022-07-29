from modules import settings
import requests
import logging

DEFAULT_SECRET = settings.HCAPTCHA_SECRET


def get_sitekey() -> str:
    return settings.HCAPTCHA_SITEKEY

def verify(captcha_response:str,secret:str = DEFAULT_SECRET) -> bool:
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
