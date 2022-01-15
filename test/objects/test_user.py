from . import clear,LOOKUP,DATA
from . import User
import unittest

class test_Create_Account(unittest.TestCase):
    def setUp(self):
        clear()

    def test_Create_User(self):
        userID = User.create(**DATA.USER)
        self.assertIsInstance(userID,int,"Didn't return interger ID")
        
        user = User.get(id=userID)
        self.assertEquals(user["name"], DATA.USER['name'])
        self.assertEquals(user["private"]["email"], DATA.USER['email'])
        
        for key,value in user.items():
            self.assertIn(key,LOOKUP.USER,f"Invalid Key '{key}' inside User")
            self.assertIsInstance(value,LOOKUP.USER[key])
