import unittest

from modules import validate


class test_md5(unittest.TestCase):
    def test_valid(self):
        valid = [
            ("c3499c2729730a7f807efb8676a92dcb","Lowercase"),
            ("C3499C2729730A7F807EFB8676A92DCB","Uppercase"),
            ("c3499c2729730A7F807EFB8676A92Dcb","MixedCase"),
        ]
        for valid,reason in valid:
            self.assertTrue(validate.md5(valid),reason)
    
    def test_invalid(self):
        invalid = [
            ("c3499C2729730a7F807EdB8676A92DC", "Too Short"),
            ("c3499C2729730a7F807EdB8676A92DCDD", "Too Long"),
            ("c3499C2729730a7F807EdB8676A92DCG", "Wrong Char"),
        ]
        for invalid,reason in invalid:
            self.assertFalse(validate.md5(invalid),reason)


class test_sha256(unittest.TestCase):
    def test_valid(self):
        valid = [
            ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340fa',"Normal")
        ]
        for valid,reason in valid:
            self.assertTrue(validate.sha256(valid),reason)
    
    def test_invalid(self):
        invalid = [
            ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340faa',"Too Long"),
            ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340f',"Too Short"),
            ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340fG',"Wrong Char"),
        ]
        for invalid,reason in invalid:
            self.assertFalse(validate.sha256(invalid),reason)


class test_url(unittest.TestCase):
    def test_valid(self):
        valid = [
            ("https://www.example.com", "Normal"),
            ("https://long.amount.of.prefix.example.com", "Many prefixes"),
            ("https://example.com", "No Prefix"),
            ("https://www.example.co.uk","double TLD"),
            ("http://www.example.com", "http"),
            ("https://www.example.com?a=2", "Parameter"),
        ]
        for valid,reason in valid:
            self.assertTrue(validate.url(valid),reason)
    
    def test_invalid(self):
        invalid = [
            ("https//example.com", "No semi-colon"),
            ("https:/example.com", "Single slash"),
            ("https://.example.com", "No prefix but has dot"),
            ("https://.com", "No Hostname, only TLD"),
            ("https://example.", "No TLD with dot"),
            ("https://example", "No TLD"),
            ("example.com", "No Protocol"),
        ]
        for invalid,reason in invalid:
            self.assertFalse(validate.url(invalid),reason)


class test_email(unittest.TestCase):
    def test_valid(self):
        valid = [
            ("david@example.com","Regular"),
            ("l@example.com","Single Character"),
        ]
        for valid,reason in valid:
            self.assertTrue(validate.email(valid),reason)
    
    def test_invalid(self):
        invalid = [
            ("@example.com","No Username"),
            ("test@example","No TLD"),
            ("test@","No Hostname"),
        ]
        for invalid,reason in invalid:
            self.assertFalse(validate.email(invalid),reason)


class test_username(unittest.TestCase):
    def test_valid(self):
        valid = [
            ('abcdefigjklmnopqrstuvwxyz',"Valid Alphabet"),
            ('0123456789_',"Valid Punctionation"),
            ('f'*4,"Min Length"),
            ('f'*32, "Max Length"),
        ]
        for valid,reason in valid:
            self.assertTrue(validate.username(valid),reason)
    
    def test_invalid(self):
        invalid = [
            ('f'*3, "Too Short"),
            ('f'*33, "Too Long"),
            ('оabcdefgh', "Homograph o"),
        ]
        for invalid,reason in invalid:
            self.assertFalse(validate.username(invalid),reason)


class test_language(unittest.TestCase):
    def test_valid(self):
        valid = [
            ("vie","Obscure"),
            ("fry","Obscure"),
            ("que","Obscure"),
            ("eng","English")
        ]
        for valid, reason in valid:
            self.assertTrue(validate.language(valid),reason)
    
    def test_invalid(self):
        invalid = [
            ('qaa', "Always Invalid Name"),
            ('english', "Full Name"),
            ('en', "ISO 639-1 code, not 3 characters"),
            ('', "Empty String"),
        ]
        for invalid,reason in invalid:
            self.assertFalse(validate.language(invalid),reason)
