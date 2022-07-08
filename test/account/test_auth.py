from . import VALID_PASSWORD
from modules.account import auth
import unittest

class test_Register_and_Signin(unittest.TestCase):
    def tearDown(self):
        auth.delete('user1')
        
    def test_Register_and_Signin(self):
        auth.register('user1',VALID_PASSWORD)
        assert auth.login('user1',VALID_PASSWORD)
        assert auth.login('user1','abc') == False
        auth.delete('user1')
        assert auth.login('user1',VALID_PASSWORD) == False


class test_Register_and_Delete(unittest.TestCase):
    def tearDown(self):
        auth.delete('user1')

    def test_Register_and_Delete(self):
        auth.register('user1',VALID_PASSWORD)
        assert auth.login('user1',VALID_PASSWORD)
        assert auth.login('user1','abc') == False


class test_Password_Changes_Updates_Password(unittest.TestCase):
    def setUp(self):
        auth.register('user1',VALID_PASSWORD)
    def tearDown(self):
        auth.delete('user1')

    def test_Password_Changes_Updates_Password(self):
        new_password = VALID_PASSWORD + 'a'
        auth.change_password('user1',new_password)
        assert auth.login('user1',VALID_PASSWORD) == False
        assert auth.login('user1',new_password) == True
