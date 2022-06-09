from modules.database import User
import unittest

generate_user = lambda:User.User(id=User.get_unique_id(),username="test")

class TestCase(unittest.TestCase):
    def tearDown(self) -> None:
        User.clear()
    def setUp(self):
        self.user = generate_user()

class test_Unique_IDs_are_Unique_After_Deletion(TestCase):
    def test_a(self):
        user = generate_user()
        User.create(user)
        User.delete(user.id)
        assert User.get_unique_id() != user.id, "Deleting User should not change the unique ID"


class test_Can_Delete_Non_Existant_Users(TestCase):
    def test_a(self):
        User.delete(1)
        User.delete(1)


class test_Cannot_Retrieve_Non_Existant_User(TestCase):
    def test_a(self):
        user = generate_user()
        User.create(user)
        User.delete(user.id)
        self.assertRaises(KeyError,User.get,user.id)

class test_User_Should_Not_be_changed_by_database(TestCase):
    def test_a(self):
        user = generate_user()
        User.create(user) 
        assert User.get(user.id) == user, "User pulled from database was not the same"


class test_User_getByEmail(unittest.TestCase):
    def setUp(self):
        self.user = generate_user()
        self.email = "foo@bar.com"
        self.user.email = self.email
        User.create(self.user)
    
    def test_a(self):
        assert User.getByEmail(self.email) == self.user

    def test_b(self):
        email = "doesntexist@bar.com"
        self.assertRaises(KeyError,User.getByEmail,email)

class test_User_getByUsernam(TestCase):
    def setUp(self):
        self.user = generate_user()
        self.name = "example_name"
        self.user.username = self.name
        User.create(self.user)
    
    def test_a(self):
        assert User.getByUsername(self.name) == self.user

    def test_b(self):
        username = "DoesntExist"
        self.assertRaises(KeyError,User.getByUsername,username)