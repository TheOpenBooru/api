from functools import cache
import re as _re
import iso639 as _iso639

USERNAME_REGEX = r"^[a-z0-9_]{4,32}$"
TAG_REGEX = r"^[_()a-z0-9]{1,32}$"
URL_REGEX = r"^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
MD5_REGEX = r"^[0-9a-fA-F]{32}$"
SHA256_REGEX = r"^[0-9a-fA-F]{64}$"


@cache
def language(country_code:str) -> bool:
    return _iso639.is_valid639_2(country_code)


@cache
def username(name: str) -> bool:
    return bool(_re.match(USERNAME_REGEX, name))


@cache
def tag(tag: str) -> bool:
    return bool(_re.match(TAG_REGEX, tag))


@cache
def url(url: str) -> bool:
    return bool(_re.match(URL_REGEX, url))


@cache
def email(email: str) -> bool:
    return bool(_re.match(EMAIL_REGEX, email))


@cache
def md5(md5: str) -> bool:
    return bool(_re.match(MD5_REGEX, md5))


@cache
def sha256(sha: str) -> bool:
    return bool(_re.match(SHA256_REGEX, sha))
