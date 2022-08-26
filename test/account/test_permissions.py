from modules.account import Permissions
import pytest


def test_Returns_Permissions_Instance():
    perms = Permissions.from_level('user')
    assert isinstance(perms,Permissions),'Permissions not an instance of Permissions'


def test_Permissions_From_Valid_Levels():
    anon = Permissions.from_level('annonymous')
    user = Permissions.from_level('user')
    admin = Permissions.from_level('user')


def test_Raise_KeyError_On_Invalid():
    with pytest.raises(KeyError):
        Permissions.from_level('invalid')


def test_Allows_Custom_Lookups():
    lookup = {
        "custom":{
            "canViewPosts":{"captcha":True,}
        }
    }
    perms = Permissions.from_level('custom',lookup)
    assert perms.hasPermission("canViewPosts")
    assert perms.isCaptchaRequired("canViewPosts")
