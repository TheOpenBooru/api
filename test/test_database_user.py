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
import pytest

def create_user(id:int):
    return schemas.User(
        id=id,
        name=f"User_{id}",
        email=f"{id}@example.com",
    )

def test_Unused_ID_is_unused(self):
    id = User.get_unused_id()
    User.get(id=id)
