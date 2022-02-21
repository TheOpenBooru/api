from modules import settings
import unittest

class test_Settings_Preserve_Correct_Value(unittest.TestCase):
    def test_a(self):
        assert settings.get('testing.value.str') == "sample text"
        assert settings.get('testing.value.int') == 64
        assert settings.get('testing.value.float') == 6.4
        assert settings.get('testing.value.bool') == False
        assert settings.get('testing.value.array') == [1,2,3]

class test_Getting_Settings_Preserve_Types(unittest.TestCase):
    def test_a(self):
        assert isinstance(settings.get('testing.type.str'),str)
        assert isinstance(settings.get('testing.type.int'),int)
        assert isinstance(settings.get('testing.type.float'),float)
        assert isinstance(settings.get('testing.type.bool'),bool)
        assert isinstance(settings.get('testing.type.array'),list)

class test_Should_Allow_Non_Terminating_Settings(unittest.TestCase):
    def test_a(self):
        assert isinstance(settings.get('testing.value'),dict)

class test_Raise_Error_On_Invalid_Setting(unittest.TestCase):
    def test_a(self):
        self.assertRaises(KeyError, settings.get, 'invalid')
        self.assertRaises(KeyError, settings.get, 'testing.invalid')
        self.assertRaises(KeyError, settings.get, 'testing.value.invalid')
