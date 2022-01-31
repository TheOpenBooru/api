import unittest
import string
from modules import validation

class test_Username(unittest.TestCase):
    def test_valid_usernames(self):
        VALID = [
            'abcdefigjklmnopqrstuvwxyz', # Valid Alphabet
            '0123456789_', # Valid Punctionation
            'f'*4, # Min Length
            'f'*32 # Max Length
            ]
        for valid in VALID:
            self.assertTrue(validation.username(valid),valid)
    
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
            self.assertFalse(validation.username(invalid),invalid)


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
            self.assertTrue(validation.url(valid),valid)
    
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
            self.assertFalse(validation.url(invalid),invalid)


class test_Email(unittest.TestCase):
    def test_invalid_emails(self):
        INVALID = [
            "@example.com",
            "test@example"
            ]
        for invalid in INVALID:
            self.assertFalse(validation.email(invalid),invalid)
        
    def test_valid_emails(self):
        VALID = [
            "david@example.com",
            "llllll@example.com"
            ]
        for valid in VALID:
            self.assertTrue(validation.email(valid),valid)


class test_MD5(unittest.TestCase):
    def test_invalid_hashes(self):
        INVALID = [
            "c3499C2729730a7F807EdB8676A92DC", # Too Short
            "c3499C2729730a7F807EdB8676A92DCDD", # Too Long
            "c3499C2729730a7F807EdB8676A92DCG", # Wrong Char
            ]
        for invalid in INVALID:
            self.assertFalse(validation.md5(invalid),invalid)
    
    def test_valid_hashes(self):
        VALID = [
            "c3499c2729730a7f807efb8676a92dcb",
            "C3499C2729730A7F807EFB8676A92DCB",
            ]
        for valid in VALID:
            self.assertTrue(validation.md5(valid),valid)


class test_SHA256(unittest.TestCase):
    def test_invalid_hashes(self):
        INVALID = [
            # Too Long
                'd04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340faa'
            # Too Short
                'd04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340f'
            # Wrong Char
                'd04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340fG'
            ]
        for invalid in INVALID:
            self.assertFalse(validation.sha256(invalid),invalid)

    def test_valid_hashes(self):
        VALID = [
            'd04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340fa'
            ]
        for valid in VALID:
            self.assertTrue(validation.sha256(valid),valid)