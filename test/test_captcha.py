from modules import captcha,settings
import unittest
import requests

TEST_KEY = "10000000-aaaa-bbbb-cccc-000000000001"
TEST_SECRET = "0x0000000000000000000000000000000000000000"
VALID_RESPONSE = "10000000-aaaa-bbbb-cccc-000000000001"
INVALID_RESPONSE = "12345678-abcd-abcd-abcd-123456789012"


try:
    requests.get("https://hcaptcha.com/siteverify",timeout=1)
except Exception:
    CAN_CONNECT = False
else:
    CAN_CONNECT = True


@unittest.skipUnless(CAN_CONNECT,"Cannot contact hcaptcha api")
class test_captcha_verify(unittest.TestCase):
    def test_verifies_valid_responses(self):
        success = captcha.verify(VALID_RESPONSE, TEST_SECRET)
        assert success, "Didn't validate test key"
    
    def test_denies_valid_responses(self):
        success = captcha.verify(INVALID_RESPONSE, TEST_SECRET)
        assert success == False, "Validated bad response"