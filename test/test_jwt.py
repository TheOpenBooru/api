from modules import jwt
import time
import unittest


class test_Tokens_Are_Strings(unittest.TestCase):
    def test_Tokens_Are_Strings(self):
        token = jwt.create({})
        assert isinstance(token,str)

class test_Tokens_Should_Expire(unittest.TestCase):
    def test_Tokens_Expire(self):
        token = jwt.create({},expiration=-1)
        self.assertRaises(jwt.BadTokenError,jwt.decode,token)
    
    def test_Token_Dont_Expire_Early(self):
        token = jwt.create({},expiration=10)
        jwt.decode(token)

class test_Data_From_Tokens_Should_Be_Unchanged(unittest.TestCase):
    def test_Token_Stores_Data(self):
        data = {'a':'100','b':200,'c':0.201,'4':True}
        token = jwt.create(data)
        assert jwt.decode(token) == data

class test_Shouldnt_Accept_Reserved_Keys(unittest.TestCase):
    def test_Expiration(self):
        data = {'exp':time.time() + 5}
        self.assertRaises(ValueError,jwt.create,data)

class test_None_Alogirthm_Should_Not_Be_Accepted(unittest.TestCase):
    def test_None_Algorithm_Should_Not_Be_Accepted(self):
        TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJhIjoxfQ."
        self.assertRaises(jwt.BadTokenError,jwt.decode,TOKEN)