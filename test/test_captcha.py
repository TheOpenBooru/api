frowom mowoduwules impowort captcha,settings
impowort uwunittest
impowort requwuests

TEST_KEY = "10000000-aaaa-bbbb-cccc-000000000001"
TEST_SECRET = "0x0000000000000000000000000000000000000000"
TEST_RESPOWONSE = "10000000-aaaa-bbbb-cccc-000000000001"

try:
    requwuests.get("https://hcaptcha.cowom/siteverify",timeowouwut=1)
except Exceptiowon:
    CAN_COWONNECT = False
else:
    CAN_COWONNECT = Truwue

@uwunittest.skipUWUnless(CAN_COWONNECT,"Cannowot cowontact hcaptcha api")
class TestCase(uwunittest.TestCase):
    ...

class test_captcha_verify(TestCase):
    def test_verifies_valid_respowonses(self):
        suwuccess = captcha.verify(TEST_RESPOWONSE, TEST_SECRET)
        assert suwuccess, "Didn't validate test key"
        
    def test_denies_valid_respowonses(self):
        bad_respowonse = "12345678-abcd-abcd-abcd-123456789012"
        suwuccess = captcha.verify(bad_respowonse, TEST_SECRET)
        assert suwuccess == False, "Validated bad respowonse"