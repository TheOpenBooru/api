from openbooru.modules import jwt
import time
import pytest


def test_Tokens_Are_Strings():
    token = jwt.create({})
    assert isinstance(token,str)

def test_Tokens_Expire():
    token = jwt.create({},expiration=-1)
    with pytest.raises(jwt.BadTokenError):
        jwt.decode(token)
    
def test_Token_Dont_Expire_Early():
    token = jwt.create({},expiration=10)
    jwt.decode(token)

def test_Token_Stores_Data():
    data = {'a':'100','b':200,'c':0.201,'4':True}
    token = jwt.create(data)
    assert jwt.decode(token) == data

def test_Shouldnt_Accept_Reserved_Keys():
    data = {'exp':time.time() + 5}
    with pytest.raises(ValueError):
        jwt.create(data)

def test_None_Algorithm_Should_Not_Be_Accepted():
    TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJhIjoxfQ."
    with pytest.raises(jwt.BadTokenError):
        jwt.decode(TOKEN)