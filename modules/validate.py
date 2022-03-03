import re as _re
import iso639 as _iso639

import string as _string

USERNAME_REGEX = r"^[a-z0-9_]{4,32}$"
def username(name: str):
    if _re.match(USERNAME_REGEX, name):
        return True
    else:
        return False

TAG_REGEX = r"^[a-z0-9_()]{1,64}$"
def tag(tag: str) -> bool:
    if _re.match(TAG_REGEX, tag):
        return True
    else:
        return False


RATING_REGEX = r"^(safe|questionable|explicit)$"
def rating(rating:str):
    if _re.match(RATING_REGEX, rating):
        return True
    else:
        return False

TYPE_REGEX = r"^(image|gif|video)$"
def post_type(type:str):
    if _re.match(TYPE_REGEX, type):
        return True
    else:
        return False


def language(country_code:str):
    return _iso639.is_valid639_2(country_code)


URL_REGEX = r"^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
def url(url: str):
    if _re.match(URL_REGEX, url):
        return True
    else:
        return False


EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
def email(email: str):
    if _re.match(EMAIL_REGEX, email):
        return True
    else:
        return False


MD5_REGEX = r"^[0-9a-fA-F]{32}$"
def md5(md5: str):
    if _re.match(MD5_REGEX, md5):
        return True
    else:
        return False


SHA256_REGEX = r"^[0-9a-fA-F]{64}$"
def sha256(sha: str):
    if _re.match(SHA256_REGEX, sha):
        return True
    else:
        return False
