import pytest
from openbooru.modules import schemas, database

@pytest.fixture
def ExampleUser() -> schemas.User:
    id = database.User.get_unique_id()
    user = schemas.User(
        id=id,
        username="ExampleUser",
        email="user@example.com",
    )
    database.User.insert(user)
    return user