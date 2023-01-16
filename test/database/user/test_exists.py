from . import ExampleUser
from modules import schemas
from modules.database import User
from modules.database.User import exists, existsByEmail, existsByUsername
import unittest


class test_Exists(unittest.TestCase):
    def setUp(self) -> None:
        self.user = schemas.User(
            id=User.get_unique_id(),
            username="ExampleUser",
            email="user@example.com",
        )
        User.insert(self.user)
    
    def tearDown(self) -> None:
        User.clear()
    
    def test_exists(self):
        id = self.user.id
        assert User.exists(id), "Exists could not detect user"
        assert User.exists(99999999) == False, "Exists passed non-existant user"


    def test_existsByUsername(self):
        name = self.user.username
        assert User.existsByUsername(name), "existsByUsername could not detect user based on name"
        assert User.existsByUsername("INVALID_USER") == False, "existsByUsername detected user that didn't exist"



    def test_existsByEmail(self):
        name = self.user.email
        assert User.existsByEmail(name), "existsByEmail could not detect user based on email"
        assert User.existsByEmail("invalid@example.com") == False, "existsByEmail detected user that didn't exist"
        assert User.existsByEmail(None) == False, "existsByEmail detected email for None"
