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
generateRandomID = random.randint(0,1000000)
class test_Can_Create_Accounts(unittest.TestCase):
    def tearDown(self) -> None:
        user.clear()
    def test_a(self):
        user.create(1,VALID_PASSWORD)

class test_Sign_In_With_Correct_Passwrord(unittest.TestCase):
    def tearDown(self) -> None:
        user.clear()
    def test_a(self):
        user.create(1,VALID_PASSWORD)
        self.assertTrue(user.login(1,VALID_PASSWORD))

class test_Prevent_Sign_In_With_Wrong_Password(unittest.TestCase):
    def tearDown(self) -> None:
        user.clear()
    def test_a(self):
        user.create(1,VALID_PASSWORD+'i')
        self.assertFalse(user.login(1,VALID_PASSWORD+'1'))

class test_Password_Update_Changes_Password(unittest.TestCase):
    def tearDown(self) -> None:
        user.clear()
    def test_Changing_P(self):
        Pass_a = VALID_PASSWORD
        Pass_b = VALID_PASSWORD+'a'
        user.create(1,Pass_a)
        user.change_password(1,Pass_b)
        self.assertFalse(user.login(1,Pass_a))
        self.assertTrue(user.login(1,Pass_b))

class test_Password_Change_Failed(unittest.TestCase):
    def tearDown(self) -> None:
        user.clear()
    def test_Password_Isnt_Changed_On_Failure(self):
        user.create(1,VALID_PASSWORD)
        self.assertRaises(ValueError,user.change_password,1,'a')
        self.assertTrue(user.login(1,VALID_PASSWORD))
        self.assertFalse(user.login(1,'a'))


class test_User_Create_Rejects_Long_Passwords(unittest.TestCase):
    def tearDown(self) -> None:
        user.clear()
    def test_User_Create_Rejects_Long_Passwords(self):
        self.assertRaises(ValueError,user.create,1,'f' * 129)

class test_Change_Password_Rejects_Long_Passwords(unittest.TestCase):
    def tearDown(self) -> None:
        user.clear()
    def test_Change_Password_Rejects_Long_Passwords(self):
        user.create(1,VALID_PASSWORD)
        self.assertRaises(ValueError,user.change_password,1,'f' * 129)

class test_Reject_Under_Passwords(unittest.TestCase):
    def tearDown(self) -> None:
        user.clear()
    def test_User_Create_Rejects_Short_Passwords(self):
        self.assertRaises(ValueError,user.create,1,'f' * 7)

class test_Change_Password_Rejects_Short_Passwords(unittest.TestCase):
    def tearDown(self) -> None:
        user.clear()
    def test_Change_Password_Rejects_Short_Passwords(self):
        user.create(1,VALID_PASSWORD)
        self.assertRaises(ValueError,user.change_password,1,'f' * 7)
