import json
import pytest
from modules import schemas, database

with open('data/test/sample_data.json','r') as f:
    TESTDATA = json.load(f)

TEST_VIDEO = TESTDATA['video']['heavy']
TEST_ANIMATION = TESTDATA['animation']['Transparent']
TEST_IMAGE = TESTDATA['image']['Small']

@pytest.fixture
def ExampleTag() -> schemas.Tag:
    return schemas.Tag(name="test")


@pytest.fixture
def ClearDatabase():
    database.clear()


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
        media_type=schemas.MediaType.image,
        full=image,
        thumbnail=image
    )
    return post
