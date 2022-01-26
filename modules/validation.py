import re
import string
import unittest

class Validate:
    @staticmethod
    def username(name:str) -> bool:
        VALID_CHARS = string.ascii_letters + string.digits + '_'
        if not(3 < len(name) <= 32):
            return False # Unacceptable Length
        elif sum([x not in VALID_CHARS for x in name]):
            return False # Unacceptable Characters
        else:
            return True

    @staticmethod
    def url(email:str) -> bool:
        REGEX = r"(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?"
        return bool(re.match(REGEX,email))

    @staticmethod
    def email(email:str) -> bool:
        REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(REGEX,email))

    @staticmethod
    def md5(md5:str) -> bool:
        REGEX = r"^([0-9a-f]{32}|[A-F0-9]{32})$"
        return bool(re.match(REGEX,md5))

    @staticmethod
    def sha1(sha:str) -> bool:
        REGEX = r"^([0-9a-f]{40}|[A-F0-9]{40})$"
        return bool(re.match(REGEX,sha))