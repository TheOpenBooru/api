from . import VALID_PASSWORD
from modules import account
import pytest


def test_Register_Already_Existant_Account(WipeAuth):
    account.register("User1",VALID_PASSWORD)
    with pytest.raises(account.AccountAlreadyExists):
        account.register("User1",VALID_PASSWORD)


def test_Cannot_Register_With_Bad_Password(WipeAuth):
    account.clear()
    with pytest.raises(account.InvalidPassword):
        account.register("User1","")


def test_Login_Raises_AccountDoesNotExist():
    with pytest.raises(account.AccountDoesntExists):
        account.login("INVALID_ACCOUNT","")


