from modules import jwt
import time
import unittest


class test_Tokens_Are_Strings(unittest.TestCase):
    def test_Tokens_Are_Strings(self):
        token = jwt.create(0)
        assert isinstance(token,str)

class test_Tokens_Should_Expire(unittest.TestCase):
    def test_Tokens_Expire(self):
        token = jwt.create(0,expiration=1)
        time.sleep(2)
        self.assertRaises(jwt.BadTokenError,jwt.decode,token)
    
    def test_Token_Dont_Expire_Early(self):
        token = jwt.create(0,expiration=10)
        jwt.decode(token)

class test_Data_From_Tokens_Should_Be_Unchanged(unittest.TestCase):
    def test_Token_Stores_Data(self):
        data = {'a':'100','b':200,'c':0.201,'4':True}
        token = jwt.create(123456,additional_data=data)
        tokenData = jwt.decode(token)
        assert tokenData.data == data

class test_UserID_From_Tokens_Should_Be_Unchanged(unittest.TestCase):
    def test_Token_Stores_User_ID(self):
        token = jwt.create(12038)
        tokenData = jwt.decode(token)
        assert tokenData.userID == 12038

class test_Shouldnt_Accept_Reserved_Keys(unittest.TestCase):
    def test_User_ID(self):
        data = {'_user_id':4}
        self.assertRaises(ValueError,jwt.create,0,data)
    def test_Expiration(self):
        data = {'exp':time.time() + 5}
        self.assertRaises(ValueError,jwt.create,0,data)

class test_None_Alogirthm_Should_Not_Be_Accepted(unittest.TestCase):
    def test_None_Algorithm_Should_Not_Be_Accepted(self):
        TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJhIjoxfQ."
        self.assertRaises(jwt.BadTokenError,jwt.decode,TOKEN)