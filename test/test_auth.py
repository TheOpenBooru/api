from modules.account import auth
import time
from tqdm import tqdm
import unittest
import random

VALID_PASSWORD = r"MZR}tmL{,#:vmC'__\BTw#x2aVq+\Q{)"

class test_cant_register_user_twice(unittest.TestCase):
    def setUp(self):
        auth.register('user1',VALID_PASSWORD)
    
    def tearDown(self):
        auth.delete('user1')
    
    def test_cant_register_user_twice(self):
        with self.assertRaises(KeyError):
            auth.register('user1',VALID_PASSWORD)


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
    
    
    def test_Register_and_Signin(self):
        auth.register('user1',VALID_PASSWORD)
        assert auth.login('user1',VALID_PASSWORD)
        assert auth.login('user1','abc') == False

class test_Password_Changes_Updates_Password(unittest.TestCase):
    def setUp(self):
        auth.register('user1',VALID_PASSWORD)
    def tearDown(self):
        auth.delete('user1')
    
    def test_Register_and_Signin(self):
        new_password = VALID_PASSWORD + 'a'
        auth.change_password('user1',new_password)
        assert auth.login('user1',VALID_PASSWORD) == False
        assert auth.login('user1',new_password) == True
