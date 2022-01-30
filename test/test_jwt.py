"""Requirements:
- Tokens should be strings
- Tokens should store the provided data
- Decoded Tokens should be a dictionary
- Decoded Tokens should contain the user_id
- Tokens should overide any existing user_id field
- Tokens should expire after selected duration
- Expired Tokens should not be accepted
"""


from modules.auth import jwt
import time
import unittest


class test_Tokens_Are_Strings(unittest.TestCase):
    def test_Tokens_Are_Strings(self):
        token = jwt.create(0)
        self.assertIsInstance(token, str)

class test_Tokens_Expire_Correctly(unittest.TestCase):
    def test_Token_Can_Expire(self):
        token = jwt.create(0,expiration=0)
        time.sleep(2)
        self.assertRaises(jwt.BadTokenError,jwt.decode,token)
    
    def test_Token_Shouldnt_Expire_Early(self):
        token = jwt.create(0,expiration=10)
        jwt.decode(token)

class test_Tokens_Store_Data(unittest.TestCase):
    def test_Token_Stores_Data(self):
        data = {'a':'100','b':200,'c':True}
        token = jwt.create(1,data=data)
        self.assertEquals(jwt.decode(token),data | {'user_id':1})

class test_Tokens_Store_User_ID(unittest.TestCase):
    def test_Token_Stores_User_ID(self):
        token = jwt.create(1)
        self.assertEquals(jwt.decode(token)['user_id'],1)
    
    def test_Tokens_Overide_Data_User_ID(self):
        data = {'user_id':4}
        token = jwt.create(1,data=data)
        self.assertEquals(jwt.decode(token)['user_id'],1)

class test_Tokens_Prevent_Invalid_Data(unittest.TestCase):
    def test_Token_Store_Invalid_Data(self):
        data = {'a':id}
        self.assertRaises(TypeError,jwt.create,1,data=data)