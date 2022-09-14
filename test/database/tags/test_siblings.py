from modules import database, schemas
from modules.database import Tag
import pytest


@pytest.fixture
def ExampleTag() -> schemas.Tag:
    if Tag.exists("test"):
        Tag.delete("test")

    tag = schemas.Tag(name="test")
    Tag.insert(tag)
    return tag


def test_Add_Sibling(ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    siblingName = "test_2"
    Tag.addSibling(tagName,siblingName)
    assert Tag.get("test").siblings == [siblingName]


def test_Remove_Sibling(ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    siblingName = "test_2"
    Tag.addSibling(tagName,siblingName)
    Tag.removeSibling(tagName,siblingName)
    assert Tag.get("test").siblings == []


def test_Adding_Sibling_Is_Idempotent(ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    siblingName = "test_2"
    Tag.addSibling(tagName,siblingName)
    Tag.addSibling(tagName,siblingName)
    assert Tag.get("test").siblings == [siblingName]


def test_Removing_Sibling_Is_Idempotent(ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    Tag.removeSibling(tagName,"test_2")
    assert Tag.get("test").siblings == []


def test_Tag_Siblings_Search():
    database.Tag.clear()
    database.Post.clear()
    database.Tag.insert(schemas.Tag(
        name="mario_(super_mario)",
    ))
    database.Tag.insert(schemas.Tag(
        name="mario", siblings=["mario_(super_mario)"]
    ))
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
        thumbnail=image,
        tags=["mario"]
    )
    database.Post.insert(post)

    assert post in database.Post.search(schemas.PostQuery(
        include_tags=["mario_(super_mario)"]
    ))
    
    assert post in database.Post.search(schemas.PostQuery(
        include_tags=["mario"]
    ))