import pytest
from openbooru.modules import users

VALID_PASSWORD = r"MZR}tmL{,#:vmC'__\BTw#x2aVq+\Q{)"

@pytest.fixture
def WipeDB():
    users.clear()

def test_Register_Already_Existant_Account(WipeDB):
    users.create("User1",VALID_PASSWORD)
    with pytest.raises(users.UsernameAlreadyExists):
        users.create("User1",VALID_PASSWORD)


def test_Cannot_Register_With_Bad_Password(WipeDB):
    with pytest.raises(users.InvalidPassword):
        users.create("User1","")

