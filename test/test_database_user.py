from modules.database import User
import unittest

generate_user = lambda:User.User(id=User.get_unique_id(),username="test")

class test_Unique_IDs_are_Unique_After_Deletion(unittest.TestCase):
    def test_a(self):
        user = generate_user()
        User.create(user)
        User.delete(user.id)
        assert User.get_unique_id() != user.id, "Deleting User should not change the unique ID"


class test_Can_Delete_Non_Existant_Users(unittest.TestCase):
    def test_a(self):
        User.delete(1)
        User.delete(1)


class test_Cannot_Retrieve_Non_Existant_User(unittest.TestCase):
    def test_a(self):
        user = generate_user()
        User.create(user)
        User.delete(user.id)
        self.assertRaises(KeyError,User.get,user.id)

class test_User_Should_Not_be_changed_by_database(unittest.TestCase):
    def test_a(self):
        user = generate_user()
        User.create(user) 
        assert User.get(user.id) == user, "User pulled from database was not the same"
