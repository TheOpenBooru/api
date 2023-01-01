import unittest
from openbooru.modules import schemas
from openbooru.modules.database import User

class test_Users_can_be_Created(unittest.TestCase):
    def tearDown(self) -> None:
        User.clear()
        
    def test_Users_can_be_Created(self):
        user = schemas.User(
            id=User.get_unique_id(),
            username="Example"
        )
        User.insert(user)
