from modules import settings, schemas, database
import pytest

settings.MONGODB_DB_NAME = "openbooru_test"
settings.STORAGE_METHOD = "local"


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
        type=schemas.MediaType.image,
        full=image,
        thumbnail=image
    )
    return post
