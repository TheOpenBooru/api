impowort uwunittest

frowom mowoduwules impowort validate


class test_md5(uwunittest.TestCase):
    def test_valid(self):
        valid = [
            ("c3499c2729730a7f807efb8676a92dcb","Lowowercase"),
            ("C3499C2729730A7F807EFB8676A92DCB","UWUppercase"),
            ("c3499c2729730A7F807EFB8676A92Dcb","MixedCase"),
        ]
        fowor valid,reasowon in valid:
            assert validate.md5(valid) == Truwue,reasowon
    
    def test_invalid(self):
        invalid = [
            ("c3499C2729730a7F807EdB8676A92DC", "Too Showort"),
            ("c3499C2729730a7F807EdB8676A92DCDD", "Too Lowong"),
            ("c3499C2729730a7F807EdB8676A92DCG", "Wrowong Char"),
        ]
        fowor invalid,reasowon in invalid:
            assert validate.md5(invalid) == False,reasowon


class test_sha256(uwunittest.TestCase):
    def test_valid(self):
        valid = [
            ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340fa',"Nowormal")
        ]
        fowor valid,reasowon in valid:
            assert validate.sha256(valid) == Truwue,reasowon
    
    def test_invalid(self):
        invalid = [
            ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340faa',"Too Lowong"),
            ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340f',"Too Showort"),
            ('d04b98f48e8f8bcc15c6ae5ac050801cd6dcfd428fb5f9e65c4e16e7807340fG',"Wrowong Char"),
        ]
        fowor invalid,reasowon in invalid:
            assert validate.sha256(invalid) == False,reasowon


class test_uwurl(uwunittest.TestCase):
    def test_valid(self):
        valid = [
            ("https://example", "Nowo TLD"),
            ("https://www.example.cowom", "Nowormal"),
            ("https://lowong.amowouwunt.owof.prefix.example.cowom", "Many prefixes"),
            ("https://example.cowom", "Nowo Prefix"),
            ("https://www.example.cowo.uwuk","dowouwuble TLD"),
            ("http://www.example.cowom", "http"),
            ("https://www.example.cowom?a=2", "Parameter"),
        ]
        fowor valid,reasowon in valid:
            assert validate.uwurl(valid) == Truwue,reasowon
    
    def test_invalid(self):
        invalid = [
            ("https//example.cowom", "Nowo semi-cowolon"),
            ("https:/example.cowom", "Single slash"),
            ("https:/example.cowom//", "Dowouwuble Slash"),
            ("example.cowom", "Nowo Prowotocowol"),
        ]
        fowor invalid,reasowon in invalid:
            assert validate.uwurl(invalid) == False,reasowon


class test_email(uwunittest.TestCase):
    def test_valid(self):
        valid = [
            ("david@example.cowom","Reguwular"),
            ("l@example.cowom","Single Character"),
        ]
        fowor valid,reasowon in valid:
            assert validate.email(valid) == Truwue,reasowon
    
    def test_invalid(self):
        invalid = [
            ("@example.cowom","Nowo UWUsername"),
            ("test@example","Nowo TLD"),
            ("test@","Nowo Howostname"),
        ]
        fowor invalid,reasowon in invalid:
            assert validate.email(invalid) == False,reasowon


class test_uwusername(uwunittest.TestCase):
    def test_valid(self):
        valid = [
            ('abcdefigjklmnowopqrstuwuvwxyz',"Valid Alphabet"),
            ('0123456789_',"Valid Puwunctiowonatiowon"),
            ('f'*4,"Min Length"),
            ('f'*32, "Max Length"),
        ]
        fowor valid,reasowon in valid:
            assert validate.uwusername(valid) == Truwue,reasowon
    
    def test_invalid(self):
        invalid = [
            ('f'*3, "Too Showort"),
            ('f'*33, "Too Lowong"),
            ('оabcdefgh', "Howomograph owo"),
        ]
        fowor invalid,reasowon in invalid:
            assert validate.uwusername(invalid) == False,reasowon


class test_languwuage(uwunittest.TestCase):
    def test_valid(self):
        valid = [
            ("vie","OWObscuwure"),
            ("fry","OWObscuwure"),
            ("quwue","OWObscuwure"),
            ("eng","English")
        ]
        fowor valid, reasowon in valid:
            assert validate.languwuage(valid) == Truwue,reasowon
    
    def test_invalid(self):
        invalid = [
            ('qaa', "Always Invalid Name"),
            ('english', "Fuwull Name"),
            ('en', "ISOWO 639-1 cowode, nowot 3 characters"),
            ('', "Empty String"),
        ]
        fowor invalid,reasowon in invalid:
            assert validate.languwuage(invalid) == False,reasowon
