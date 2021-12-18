from . import create,login,decode,update,delete
from . import BadTokenError,AuthError
import os
import time
import random
import unittest


os.environ['TOKEN_SECRET'] = 'SECRET'
class User(object):
    def __enter__(self,*,ID=None,Pass=None):
        if not ID:
            ID = int((random.random()+1)*(10**9))
        if not Pass:
            Pass = hex(random.getrandbits(64))
        self.ID = ID
        create(ID,Pass)
        return ID,Pass

    def __exit__(self,*args):
        delete(self.ID)

class Auth_Create(unittest.TestCase):
    def test_Prevent_Duplicate_Users(self):
        with User() as (ID,Pass):
            try: create(ID,Pass)
            except KeyError: pass
            else: raise KeyError("Allowed duplicate user ID")

class Auth_Login(unittest.TestCase):
    def test_Login_User(self):
        with User() as (ID,Pass):
            login(ID,Pass)

    def test_Prevent_Login_Bad_Password(self):
        with User() as (ID,Pass):
            try: login(ID,Pass+"1")
            except AuthError: pass
            else: raise AuthError("Logged in with bad password")
    
    def test_Prevent_Duplicate_User(self):
        with User() as (ID,Pass):
            try: create(ID,Pass)
            except KeyError: pass
            else: raise KeyError("Allowed duplicate user ID")
    

class Auth_Token(unittest.TestCase):
    def test_Prevent_Expired_Auth_Tokens(self):
        with User() as (ID,Pass):
            token = login(ID,Pass,expiration=0)
            time.sleep(1)
            try: decode(token)
            except BadTokenError: pass
            else: raise BadTokenError("Allowed Expired Auth Token")


    def test_Block_Invalid_Auth_Tokens(self):
        with User() as (ID,Pass):
            try: login(ID,Pass,data=[]) #type:ignore PS: For Pylance
            except TypeError: pass
            else: raise TypeError("Allowed Bad Token Payload")

class Auth_Delete(unittest.TestCase):
    def test_Ensure_Users_Deleted_Successfully(self):
        with User() as (ID,Pass):
            token = login(ID,Pass)
            delete(ID)
            try: login(ID,Pass)
            except KeyError: pass
            else: raise KeyError("Logged In Deleted User")
            
            try: decode(token)
            except KeyError: pass
            else: raise KeyError("Decoded Deleted User Token")

class Auth_Password_Change(unittest.TestCase):
    def test_Prevent_Allow_Passwords(self):
        GOOD_PASSWORDS = ['C3KH42vbT2WLSjf27b9D']

        for x in GOOD_PASSWORDS:
            ID = int((random.random()+1)*(10**9))
            create(ID,x)
            delete(ID)

    
    def test_Prevent_Bad_Passwords(self):
        BAD_PASSWORDS = ['abc','52342','password']

        for x in BAD_PASSWORDS:
            ID = int((random.random()+1)*(10**9))
            try: create(ID,x)
            except ValueError: pass
            else: raise ValueError("Allowed Bad Password")
            delete(ID)

    
    def test_Update_User_Password(self):
        with User() as (ID,Pass):
            Pass2 = hex(random.getrandbits(64))
            update(ID,Pass,Pass2)
            try: login(ID,Pass)
            except AuthError: pass
            else: raise AuthError("Didn't Update Password Correctly")
            login(ID,Pass2)

        
    def test_Verify_Password_On_Change(self):
        with User() as (ID,Pass):
            Bad_Pass = "BAD_PASSWORD123"
            Pass2 = hex(random.getrandbits(64))
            try: update(ID,Bad_Pass,Pass2)
            except AuthError: pass
            else: raise AuthError("Didn't Update Password Correctly")
            login(ID,Pass)
            try: login(ID,Bad_Pass)
            except AuthError: pass
            else: raise AuthError("Didn't Update Password Correctly")
