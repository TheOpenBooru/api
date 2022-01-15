import unittest
from modules import Validate

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

    def test_md5(self):
        INVALID = [
            "c3499C2729730a7F807EdB8676A92DCB",
            ]
        VALID = [
            "c3499c2729730a7f807efb8676a92dcb",
            "C3499C2729730A7F807EFB8676A92DCB",
            ]
        for invalid in INVALID:
            self.assertFalse(Validate.md5(invalid),invalid)
        for valid in VALID:
            self.assertTrue(Validate.md5(valid),valid)