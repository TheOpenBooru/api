"""
Requirements:
get_unused_id:
    - IDs are unique
    - IDs are sequential
create:
    - Prevents Duplicates:
        - IDs
        - Names
        - Emails
    - Validates Data:
        - Uploader ID
        - Type
        - Rating
        - Language
update:
    - The user becomes the new version
search:
    - Orders Correctly
    - Appends at limit
    - Does not have max limit
delete:
    - Entries cannot be gotten
    - Allows deletion of non-existent entries
"""

from modules.database import User
from modules import schemas
import unittest

def create_user(id:int):
    return schemas.User(
        id=id,
        name=f"User_{id}",
        email=f"{id}@example.com",
    )

class test_Get_Unused_ID(unittest.TestCase):
    def tearDown(self):
        User.clear()
    
    def test_isnt_Used_By_User(self):
        id = User.get_unused_id()
        User.get(id=id)

class test_Delete(unittest.TestCase):
    def tearDown(self):
        User.clear()
    
    def test_isnt_Used_By_User(self):
        for _ in range(100):
            id = User.get_unused_id()
            assert User.get(id=id) == None
            user = create_user(id)
            User.create(user)
