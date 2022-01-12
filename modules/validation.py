import re
import string
import unittest

class Validate:
    @staticmethod
    def username(name:str) -> bool:
        VALID_CHARS = string.ascii_letters + string.digits + '_'
        if not(3 < len(name)  < 32):
            return False # Unacceptable Length
        elif sum([x not in VALID_CHARS for x in name]):
            return False # Unacceptable Characters
        else:
            return True

    @staticmethod
    def email(email:str) -> bool:
        # Taken From https://emailregex.com/
        REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        vaid = bool(re.search(REGEX,email))
        return vaid

    @staticmethod
    def md5(md5:str) -> bool:
        # Taken From https://regexpattern.com/md5-hash/
        REGEX = r"^([a-f\d]{32}|[A-F\d]{32})$"
        valid = bool(re.search(REGEX,md5))
        return valid

    @staticmethod
    def sha1(md5:str) -> bool:
        raise NotImplementedError

class test_Validation(unittest.TestCase):
    def test_Emails(self):
        INVALID = [
            "@example.com",
            "test@example"
            ]
        VALID = [
            "david@example.com",
            "llllll@example.com"
            ]
        for invalid in INVALID:
            self.assertFalse(Validate.email(invalid),invalid)
        for valid in VALID:
            self.assertTrue(Validate.email(valid),valid)