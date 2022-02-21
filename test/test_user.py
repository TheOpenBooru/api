"""Requirements:
-[x] Users should be able to create an account
-[x] Users should be able to sign-in with the correct password
-[x] User shouldn't be able to sign-in with the wrong password
-[x] When a password is updated, the old password should be rejected and the new one accepted
-[x] When a password update fails, the password should not be changed
-[] Functions should reject Invalid User IDs
-[] Delete prevents an account from being used
-[] Delete should accept Invalid User IDs
-[x] Passwords over 128 characters should be rejected
-[x] Passwords under 8 characters should be rejected
"""

from modules.auth import user
import unittest
import random

VALID_PASSWORD = 'example_password_for_testing'
getRandomID = lambda : random.randint(0,2**32)

class test_Can_Create_Accounts(unittest.TestCase):
    def test_a(self):
        user.create(getRandomID(),VALID_PASSWORD)

class test_Sign_In_With_Correct_Passwrord(unittest.TestCase):
    def test_a(self):
        id = getRandomID()
        user.create(id,VALID_PASSWORD)
        assert user.login(id,VALID_PASSWORD)

class test_Prevent_Sign_In_With_Wrong_Password(unittest.TestCase):
    def test_invalid_password(self):
        id = getRandomID()
        user.create(id,VALID_PASSWORD)
        assert user.login(id,VALID_PASSWORD+"_") == False
        assert user.login(id,"") == False

class test_Password_Updte_Changes_Password(unittest.TestCase):
    def test_Changing_P(self):
        ORIGINAL_PASSWORD = VALID_PASSWORD
        CHANGED_PASSWORD = VALID_PASSWORD+'a'
        id = getRandomID()
        
        user.create(id,ORIGINAL_PASSWORD)
        user.change_password(id,CHANGED_PASSWORD)
        
        assert user.login(id,ORIGINAL_PASSWORD) == False
        assert user.login(id,CHANGED_PASSWORD) == True

class test_Password_Change_Failed(unittest.TestCase):
    def test_Password_Isnt_Changed_On_Failure(self):
        id = getRandomID()
        user.create(id,VALID_PASSWORD)
        
        self.assertRaises(ValueError,user.change_password,id,'a')
        assert user.login(id,VALID_PASSWORD) == True
        assert user.login(id,'a') == False


class test_User_Create_Rejects_Long_Passwords(unittest.TestCase):
    def test_User_Create_Rejects_Long_Passwords(self):
        id = getRandomID()
        password = 'f' * 129
        self.assertRaises(ValueError,user.create,id,password)

class test_Change_Password_Rejects_Long_Passwords(unittest.TestCase):
    def test_Change_Password_Rejects_Long_Passwords(self):
        id = getRandomID()
        user.create(id,VALID_PASSWORD)
        password = 'f' * 129
        self.assertRaises(ValueError,user.change_password,id,password)

class test_Reject_Under_Passwords(unittest.TestCase):
    def test_User_Create_Rejects_Short_Passwords(self):
        id = getRandomID()
        password = 'f' * 7
        self.assertRaises(ValueError,user.create,id,password)

class test_Change_Password_Rejects_Short_Passwords(unittest.TestCase):
    def test_Change_Password_Rejects_Short_Passwords(self):
        id = getRandomID()
        password = 'f' * 7
        user.create(id,VALID_PASSWORD)
        self.assertRaises(ValueError,user.change_password,id,password)
