import re
import string

def username(name:str) -> bool:
    VALID_CHARS = string.ascii_letters + string.digits + '_'
    if not(3 < len(name) <= 32):
        return False # Unacceptable Length
    elif sum([x not in VALID_CHARS for x in name]):
        return False # Unacceptable Characters
    else:
        return True

def tag(tag:str):
    VALID_CHARS = string.ascii_letters + string.digits + '_()'
    if len(tag) <= 64:
        return False # Unacceptable Length
    elif sum([x not in VALID_CHARS for x in tag]):
        return False # Unacceptable Characters
    else:
        return True

def url(email:str) -> bool:
    REGEX = r"(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?"
    return bool(re.match(REGEX,email))

def email(email:str) -> bool:
    REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(REGEX,email))
    
def md5(md5:str) -> bool:
    REGEX = r"^([0-9a-fA-F]{32}$"
    return bool(re.match(REGEX,md5))

def sha256(sha:str) -> bool:
    REGEX = r"^([0-9a-fA-F]{64}$"
    return bool(re.match(REGEX,sha))
