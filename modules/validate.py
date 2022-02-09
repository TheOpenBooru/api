import re as _re
import string as _string


def username(name: str):
    VALID_CHARS = _string.ascii_letters + _string.digits + "_"
    if not (3 < len(name) <= 32):
        raise ValueError("Unacceptable Length")
    elif sum([x not in VALID_CHARS for x in name]):
        raise ValueError("Unacceptable Characters")


def tag(tag: str):
    VALID_CHARS = _string.ascii_letters + _string.digits + "_()"
    if 1 < len(tag) <= 64:
        raise ValueError("Unacceptable Length")
    elif sum([x not in VALID_CHARS for x in tag]):
        raise ValueError("Unacceptable Characters")


def rating(rating:str):
    valid_ratings = {"safe","questionable","explicit"}
    if rating not in valid_ratings:
        raise  ValueError("Invalid Rating Code")


def language(country_code:str):
    codes = ["eng","fra"]
    if country_code not in codes:
        raise ValueError("Invalid Language Code")



def url(url: str):
    REGEX = r"(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?"
    if not _re.match(REGEX, url):
        raise ValueError("Invalid URL")


def email(email: str):
    REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not _re.match(REGEX, email):
        raise ValueError("Invalid Email")


def md5(md5: str):
    REGEX = r"^[0-9a-fA-F]{32}$"
    if not _re.match(REGEX, md5):
        raise ValueError("Invalid MD5")


def sha256(sha: str):
    REGEX = r"^[0-9a-fA-F]{64}$"
    if not _re.match(REGEX, sha):
        raise ValueError("Invalid SHA256")
