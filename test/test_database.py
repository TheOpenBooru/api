"""Requirements:
- User's create
- User's data can be updated
- 
"""
import os
import time
import unittest
from modules.database import Post, Tag, User,types

class test_Create_User_Should_Return_A_User_Object(unittest.TestCase):
    user:types.User
    def tearDown(self):
        User.delete(self.user.id)
    def test_create(self):
        self.user = user = User.create('example_name','example@example.com')
        self.assertIsInstance(user,types.User)
        self.assertEqual(user.name, 'example_name')
        self.assertEqual(user.email, 'example@example.com')


class test_Getting_User_Should_Return_Valid_User(unittest.TestCase):
    user:types.User
    def tearDown(self):
        User.delete(self.user.id)
    def test_create(self):
        userID = User.create('example_name','example@example.com').id
        user = self.user = User.get(userID)
        self.assertIsInstance(user,types.User)
        self.assertEqual(user.name,'example_name')
        self.assertEqual(user.email,'example@example.com')

class test_Getting_User(unittest.TestCase):
    def test_delete(self):
        user = self.user = User.create('example_name','example@example.com')
        User.delete(user.id)
        self.assertRaises(KeyError,User.get,id=user.id)