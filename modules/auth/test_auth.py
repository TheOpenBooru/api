from . import create,login,verify,update,delete
from . import BadTokenError,LoginFailureError
import os
import time
import random
import unittest


os.environ['TOKEN_SECRET'] = 'SECRET'
BAD_PASSWORDS = [
    'abc',
    'password',
    '1234567890',
]
GOOD_PASSWORDS = []

getID = lambda:int((random.random()+1)*(10**9))
getPass = lambda:hex(random.getrandbits(64))

class Entry(object):
    def __enter__(self,*,ID=None,Pass=None):
        if not ID:
            ID = getID()
        if not Pass:
            Pass = getPass()
        self.ID = ID
        create(ID,Pass)
        return ID,Pass

    def __exit__(self,*args):
        delete(self.ID)


class Auth_Create(unittest.TestCase):
    def test_Create_Auth_User(self):
        create(getID(),getPass())


    def test_Prevent_Duplicate_Auth_Entries(self):
        with Entry() as (ID,Pass):
            try: create(ID,Pass)
            except KeyError: pass
            else: raise KeyError("Allowed duplicate user ID")


    def test_Prevent_Creating_Entry_With_Bad_Password(self):
        for x in BAD_PASSWORDS:
            try: create(getID(),x)
            except ValueError: pass
            else: raise ValueError("Allowed Bad Password")


class Auth_Login(unittest.TestCase):
    def test_Login_Accepts_Correct_Password(self):
        with Entry() as (ID,Pass):
            login(ID,Pass)


    def test_Login_Doesnt_Accept_Wrong_Passwords(self):
        with Entry() as (ID,Pass):
            try: login(ID,Pass+"1")
            except LoginFailureError: pass
            else: raise LoginFailureError("Allowed Log in with bad password")


class Auth_Token(unittest.TestCase):
    def test_Expired_Auth_Tokens_Are_Invalid(self):
        with Entry() as (ID,Pass):
            token = login(ID,Pass,expiration=0)
            time.sleep(1)
            try: verify(token)
            except BadTokenError: pass
            else: raise BadTokenError("Allowed Expired Auth Token")


    def test_Malformed_Auth_Tokens_Are_Invalid(self):
        with Entry() as (ID,Pass):
            try: login(ID,Pass,data=[]) #type:ignore PS: For Pylance
            except TypeError: pass
            else: raise TypeError("Allowed Bad Token Payload")


    def test_Auth_Tokens_From_Deleted_Users_Are_Invalid(self):
        with Entry() as (ID,Pass):
            token = login(ID,Pass)
            delete(ID)
            try: verify(token)
            except KeyError: pass
            else: raise KeyError("Allowed Auth Token from deleted user")


class Auth_Delete(unittest.TestCase):
    def test_Entries_Are_Deleted_Successfully(self):
        with Entry() as (ID,Pass):
            login(ID,Pass)
            delete(ID)
            try: login(ID,Pass)
            except KeyError: pass
            else: raise KeyError("Logged In Deleted User")


class Auth_Password_Change(unittest.TestCase):
    def test_Successfully_Updates_An_Entries_Password(self):
        with Entry() as (ID,Pass):
            Pass2 = hex(random.getrandbits(64))
            update(ID,Pass,Pass2)
            try: login(ID,Pass)
            except LoginFailureError: pass
            else: raise LoginFailureError("Didn't Update Password Correctly")
            login(ID,Pass2)


    def test_Prevents_Changing_Entry_To_Bad_Password(self):
        for bad_pass in BAD_PASSWORDS:
            with Entry() as (ID,Pass):
                try: update(ID,Pass,bad_pass)
                except ValueError: pass
                else: raise ValueError("Allowed Bad Password")


    def test_Change_Password_Verifes_Old_Password(self):
        with Entry() as (ID,Pass):
            Bad_Pass = "BAD_PASSWORD123"
            Pass2 = hex(random.getrandbits(64))
            try: update(ID,Bad_Pass,Pass2)
            except LoginFailureError: pass
            else: raise LoginFailureError("Allowed Invalid Password for Password Change")
            update(ID,Pass,Pass2)
