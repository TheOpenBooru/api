from modules import jwt
import time
import pytest


def test_Tokens_Are_Strings():
    token = jwt.create(0)
    assert isinstance(token,str)

def test_Tokens_Expire():
    token = jwt.create(0,expiration=1)
    time.sleep(2)
    with pytest.raises(jwt.BadTokenError):
        jwt.decode(token)

def test_Token_Dont_Expire_Early():
    token = jwt.create(0,expiration=10)
    jwt.decode(token)

def test_Data_From_Tokens_Should_Be_Unchanged():
    data = {'a':'100','b':200,'c':0.201,'4':True}
    token = jwt.create(123456,additional_data=data)
    tokenData = jwt.decode(token)
    assert tokenData.data == data

def test_UserID_From_Tokens_Should_Be_Unchanged():
    token = jwt.create(12038)
    tokenData = jwt.decode(token)
    assert tokenData.userID == 12038

def test_Shouldnt_Accept_Reserved_Keys():
    data = {
        '_user_id':4,
        'exp':time.time() + 5
    }
    with pytest.raises(ValueError):
        jwt.create(0,additional_data=data)

def test_None_Algorithm_Should_Not_Be_Accepted():
    TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJhIjoxfQ."
    with pytest.raises(jwt.BadTokenError):
        jwt.decode(TOKEN)
