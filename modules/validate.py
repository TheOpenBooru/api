import re as _re
import iso639 as _iso639
from modules import settings

USERNAME_REGEX = r"^[a-z0-9_]{4,32}$"
def username(name: str):
    if _re.match(USERNAME_REGEX, name):
        return True
    else:
        return False


def language(country_code:str):
    return _iso639.is_valid639_2(country_code)


RATING_REGEX = r"^(safe|questionable|explicit)$"
def rating(rating:str):
    return bool(_re.match(RATING_REGEX, rating))


TYPE_REGEX = r"^(image|animation|video)$"
def post_type(type:str):
    return bool(_re.match(TYPE_REGEX, type))


TAG_REGEX = r"^([a-z]{1,32}:)?[_()a-z0-9]{1,32}$"
def tag(tag: str) -> bool:
    return bool(_re.match(TAG_REGEX, tag))


URL_REGEX = r"^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
def url(url: str):
    return bool(_re.match(URL_REGEX, url))


EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
def email(email: str):
    return bool(_re.match(EMAIL_REGEX, email))


MD5_REGEX = r"^[0-9a-fA-F]{32}$"
def md5(md5: str):
    return bool(_re.match(MD5_REGEX, md5))


SHA256_REGEX = r"^[0-9a-fA-F]{64}$"
def sha256(sha: str):
    return bool(_re.match(SHA256_REGEX, sha))
