from . import create,login,verify,update,delete
import unittest
import random



a,b,c,d,e = [ 1_000_000_000 + x for x in range(5)]
password = hex(random.getrandbits(64))

class Scenarios(unittest.TestCase):
    def setUp(self):
        delete(a)
        delete(b)
        delete(c)
        delete(d)
        delete(e)
        
    def scenario_1(self):
        create(a,password)
        create(b,password)
        create(c,password)
        
        try: create(c,password)
        except KeyError: pass
        else: raise KeyError('Able to create multiple users with same id')
        
        try: create(d,'password')
        except ValueError: pass
        else: raise ValueError("Password allowed that doesn't meet requirements")

        token = login(a,password,{'data':True})
        assert token, f"Refused Sign-in"
        login(a,)
        
        data = verify(token)
        if not data:
            raise ValueError("Refused to accept valid sign-in")
        if verify('test'):
            raise ValueError("Verified invalid token")
        
        assert data['data'] == True, f'Data not preserved in Token: {data}'
    # def scenario_2(self):
