import unittest
import string
from modules import Validate

class test_Username(unittest.TestCase):
    def test_valid_usernames(self):
        VALID = [
            'abcdefigjklmnopqrstuvwxyz', # Valid Alphabet
            '0123456789_', # Valid Punctionation
            'f'*4, # Min Length
            'f'*32 # Max Length
            ]
        for valid in VALID:
            self.assertTrue(Validate.username(valid),valid)
    
    def test_invalid_usernames(self):
        INVALID = [
            'f'*3, # Too Short
            'f'*33, # Too Longo
            'оabcdefgh' # Homograph o
            ]
        for invalid_char in list(string.punctuation):
            INVALID.append('examplename' + invalid_char) # Append invalid punctionation
        INVALID.remove('examplename'+'_') # Only valid punctuation
        
        for invalid in INVALID:
            self.assertFalse(Validate.username(invalid),invalid)


class test_URL(unittest.TestCase):
    def test_invalid_urls(self):
        VALID = [
            "https://www.example.com", # Normal
            "https://long.amount.of.prefix.example.com", # Many prefixes
            "https://example.com", # No Prefix
            "https://www.example.co.uk", # double TLD
            "http://www.example.com", # http
            "https://www.example.com?a=2", # Parameter
            ]
        for valid in VALID:
            self.assertTrue(Validate.url(valid),valid)
    
    def test_valid_urls(self):
        INVALID = [
            "https//example.com", # No semi-colon
            "https:/example.com", # Single slash
            "https://.example.com", # No prefix but has dot
            "https://.com", # No Hostname, only TLD
            "https://example.", # No TLD with dot
            "https://example", # No TLD
            "example.com", # No Protocol
            ]
        for invalid in INVALID:
            self.assertFalse(Validate.url(invalid),invalid)


class test_Email(unittest.TestCase):
    def test_invalid_emails(self):
        INVALID = [
            "@example.com",
            "test@example"
            ]
        for invalid in INVALID:
            self.assertFalse(Validate.email(invalid),invalid)
        
    def test_valid_emails(self):
        VALID = [
            "david@example.com",
            "llllll@example.com"
            ]
        for valid in VALID:
            self.assertTrue(Validate.email(valid),valid)


class test_MD5(unittest.TestCase):
    def test_invalid_hashes(self):
        INVALID = [
            "c3499C2729730a7F807EdB8676A92DC", # Too Short
            "c3499C2729730a7F807EdB8676A92DCDD", # Too Long
            "c3499C2729730a7F807EdB8676A92DCG", # Wrong Char
            "c3499C2729730a7F807EdB8676A92DCB", # Mixed case
            ]
        for invalid in INVALID:
            self.assertFalse(Validate.md5(invalid),invalid)
    
    def test_valid_hashes(self):
        VALID = [
            "c3499c2729730a7f807efb8676a92dcb",
            "C3499C2729730A7F807EFB8676A92DCB",
            ]
        for valid in VALID:
            self.assertTrue(Validate.md5(valid),valid)


class test_SHA(unittest.TestCase):
    def test_invalid_hashes(self):
        INVALID = [
            'f6949a8c7d5b90b4a698660bbfb9431503fbb9955' # Too Long
            'f6949a8c7d5b90b4a698660bbfb9431503fbb99' # Too Short
            'f6949a8c7d5b90b4a698660bbfb9431503fbb99G' # Wrong Char
            'f6949a8c7d5b90b4a698660bbfb9431503fbB99' # Mixed Case
            ]
        for invalid in INVALID:
            self.assertFalse(Validate.sha1(invalid),invalid)

    def test_valid_hashes(self):
        VALID = [
            'f6949a8c7d5b90b4a698660bbfb9431503fbb995'
            ]
        for valid in VALID:
            self.assertTrue(Validate.sha1(valid),valid)