import unittest
import string
from modules import Validate

class test_Validation(unittest.TestCase):
    def test_username(self):
        VALID = [
            'abcdefigjklmnopqrstuvwxyz', # Valid Alphabet
            '0123456789_', # Valid Punctionation
            'f'*4, # Min Length
            'f'*32 # Max Length
            ]
        INVALID = [
            'f'*3, # Too Short
            'f'*33, # Too Longo
            'оabcdefgh' # Homograph o
            ]
        for invalid_char in list(string.punctuation):
            INVALID.append(VALID[0] + invalid_char) # Append invalid punctionation
        INVALID.remove(VALID[0]+'_') # Only valid punctuation
        
        for valid in VALID:
            self.assertTrue(Validate.username(valid),valid)
        for invalid in INVALID:
            self.assertFalse(Validate.username(invalid),invalid)
    
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
            "c3499C2729730a7F807EdB8676A92DC", # Too Short
            "c3499C2729730a7F807EdB8676A92DCDD", # Too Long
            "c3499C2729730a7F807EdB8676A92DCG", # Wrong Char
            "c3499C2729730a7F807EdB8676A92DCB", # Mixed case
            ]
        VALID = [
            "c3499c2729730a7f807efb8676a92dcb",
            "C3499C2729730A7F807EFB8676A92DCB",
            ]
        for invalid in INVALID:
            self.assertFalse(Validate.md5(invalid),invalid)
        for valid in VALID:
            self.assertTrue(Validate.md5(valid),valid)
    
    def test_sha(self):
        INVALID = [
            'f6949a8c7d5b90b4a698660bbfb9431503fbb9955' # Too Long
            'f6949a8c7d5b90b4a698660bbfb9431503fbb99' # Too Short
            'f6949a8c7d5b90b4a698660bbfb9431503fbb99G' # Wrong Char
            'f6949a8c7d5b90b4a698660bbfb9431503fbB99' # Mixed Case
            ]
        VALID = [
            'f6949a8c7d5b90b4a698660bbfb9431503fbb995'
            ]
        for invalid in INVALID:
            self.assertFalse(Validate.sha1(invalid),invalid)
        for valid in VALID:
            self.assertTrue(Validate.sha1(valid),valid)