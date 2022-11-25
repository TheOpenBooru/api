from . import VALID_PASSWORD
from modules import account
import pytest

def test_Login_Raises_AccountDoesNotExist():
    with pytest.raises(account.AccountDoesntExists):
        account.login("INVALID_ACCOUNT", VALID_PASSWORD)
