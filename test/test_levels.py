from modules.levels import Permissions,permissions_from_level


def test_Returns_Permissions_Instance():
    perms = permissions_from_level('user')
    assert isinstance(perms,Permissions),'Permissions not an instance of Permissions'

def test_Level_Is_Case_Insensitive():
    a = permissions_from_level('user')
    b = permissions_from_level('User')
    c = permissions_from_level('USER')
    assert a == b == c, "Levels are not case insensitive"

def test_Permissions_From_Valid_Levels():
    anon = permissions_from_level('annonymous')
    user = permissions_from_level('user')
    admin = permissions_from_level('user')

def test_Raise_KeyError_On_Invalid():
    self.assertRaises(KeyError,permissions_from_level,'invalid')
