from modules.database import Tag 
import pytest



@pytest.fixture
def ExampleTag() -> Tag.Tag:
    if Tag.exists("test"):
        Tag.delete("test")
    
    Tag.create("test")
    return Tag.get("test")


def test_AddSibling(ExampleTag:Tag.Tag):
    tagName = ExampleTag.name
    siblingName = "test_2"
    Tag.addSibling(tagName,siblingName)
    assert Tag.get("test").siblings == [siblingName]

def test_RemoveSibling(ExampleTag:Tag.Tag):
    tagName = ExampleTag.name
    siblingName = "test_2"
    Tag.addSibling(tagName,siblingName)
    Tag.removeSibling(tagName,siblingName)
    assert Tag.get("test").siblings == []


def test_AddingSiblingIsIdempotent(ExampleTag:Tag.Tag):
    tagName = ExampleTag.name
    siblingName = "test_2"
    Tag.addSibling(tagName,siblingName)
    Tag.addSibling(tagName,siblingName)
    assert Tag.get("test").siblings == [siblingName]

def test_RemovingSiblingIsIdempotent(ExampleTag:Tag.Tag):
    tagName = ExampleTag.name
    Tag.removeSibling(tagName,"test_2")
    assert Tag.get("test").siblings == []