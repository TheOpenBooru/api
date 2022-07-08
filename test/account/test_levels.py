from modules.account.levels import UserPermissions,permissions_from_level
import unittest


class test_Permissions_From_Level(unittest.TestCase):
    def test_Returns_Permissions_Instance(self):
        perms = permissions_from_level('user')
        assert isinstance(perms,UserPermissions),'Permissions not an instance of Permissions'
    
    def test_Permissions_From_Valid_Levels(self):
        anon = permissions_from_level('annonymous')
        user = permissions_from_level('user')
        admin = permissions_from_level('user')
    
    def test_Raise_KeyError_On_Invalid(self):
        self.assertRaises(KeyError,permissions_from_level,'invalid')
