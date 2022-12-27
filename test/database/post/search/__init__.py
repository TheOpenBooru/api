import pytest
from modules import database, schemas, settings
settings.POSTS_SEARCH_USE_SIBLINGS_AND_PARENTS = True

@pytest.fixture
def ExampleTag() -> schemas.Tag:
    return schemas.Tag(name="test")


def generate_post() -> schemas.Post:
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


@pytest.fixture
def ExamplePost() -> schemas.Post:
    return generate_post()


def assertPostInSearch(post_id:int, search_response:list[schemas.Post]):
    assert post_id in [x.id for x in search_response]