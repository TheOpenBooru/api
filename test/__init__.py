from modules import settings, schemas
import pytest

settings.MONGODB_DB_NAME = "openbooru_test"
settings.STORAGE_METHOD = "local"

from modules import database

@pytest.fixture
def ExampleTag() -> schemas.Tag:
    return schemas.Tag(name="test")


@pytest.fixture
def ExamplePost() -> schemas.Post:
    image = schemas.Image(
        width=1,
        height=1,
        mimetype="image/png",
        url=""
    )
    post = schemas.Post(
        id=database.Post.generate_id(),
        full=image,
        thumbnail=image
    )
    return post
