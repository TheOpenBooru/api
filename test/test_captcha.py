import unittest
from modules import captcha

test_key = "10000000-aaaa-bbbb-cccc-000000000001"
test_secret = "0x0000000000000000000000000000000000000000"
test_response = "10000000-aaaa-bbbb-cccc-000000000001"

class test_captcha_verify(unittest.TestCase):
    def test_verifies_valid_responses(self):
        success = captcha.verify(test_response, test_secret)
        assert success, "Didn't validate test key"
        
    def test_denies_valid_responses(self):
        bad_response = "12345678-abcd-abcd-abcd-123456789012"
        success = captcha.verify(bad_response, test_secret)
        assert success == False, "Validated bad response"