from modules import settings
import unittest

class test_Settings_Preserve_Correct_Value(unittest.TestCase):
    def test_a(self):
        self.assertEqual(settings.get('testing.value.str'),"sample text")
        self.assertEqual(settings.get('testing.value.int'),64)
        self.assertEqual(settings.get('testing.value.float'),6.4)
        self.assertEqual(settings.get('testing.value.bool'),False)
        self.assertEqual(settings.get('testing.value.array'),[1,2,3])

class test_Getting_Settings_Preserve_Types(unittest.TestCase):
    def test_a(self):
        self.assertIsInstance(settings.get('testing.type.str'),str)
        self.assertIsInstance(settings.get('testing.type.int'),int)
        self.assertIsInstance(settings.get('testing.type.float'),float)
        self.assertIsInstance(settings.get('testing.type.bool'),bool)
        self.assertIsInstance(settings.get('testing.type.array'),list)

class test_Raise_Error_On_Non_Ending_Setting(unittest.TestCase):
    def test_a(self):
        self.assertRaises(KeyError, settings.get, 'testing.value')

class test_Raise_Error_On_Invalid_Setting(unittest.TestCase):
    def test_a(self):
        self.assertRaises(KeyError, settings.get, 'invalid')
        self.assertRaises(KeyError, settings.get, 'testing.invalid')
        self.assertRaises(KeyError, settings.get, 'testing.value.invalid')
