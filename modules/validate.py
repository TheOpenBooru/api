import re as _re
import iso639 as _iso639

import string as _string


def username(name: str):
    REGEX = r"^[a-z0-9_]{4,32}$"
    if _re.match(REGEX, name):
        return True
    else:
        return False


def tag(tag: str) -> bool:
    REGEX = r"^[a-z0-9_()]{1,64}$"
    if _re.match(REGEX, tag):
        return True
    else:
        return False


def rating(rating:str):
    REGEX = r"(safe|questionable|explicit)"
    if _re.match(REGEX, rating):
        return True
    else:
        return False


def language(country_code:str):
    return _iso639.is_valid639_2(country_code)


def url(url: str):
    REGEX = r"(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?"
    if _re.match(REGEX, url):
        return True
    else:
        return False


def email(email: str):
    REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if _re.match(REGEX, email):
        return True
    else:
        return False


def md5(md5: str):
    REGEX = r"^[0-9a-fA-F]{32}$"
    if _re.match(REGEX, md5):
        return True
    else:
        return False


def sha256(sha: str):
    REGEX = r"^[0-9a-fA-F]{64}$"
    if _re.match(REGEX, sha):
        return True
    else:
        return False
