from . import ExamplePost, ExampleTag
from openbooru.modules import database, schemas


def test_Add_Parent(ExampleTag:schemas.Tag):
    database.clear()
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.addParent(tagName, "parent")
    assert database.Tag.get("test").parents == ["parent"]


def test_Remove_Parent(ExampleTag:schemas.Tag):
    database.clear()
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.addParent(tagName,"parent")
    database.Tag.removeParent(tagName,"parent")
    assert database.Tag.get("test").parents == []


def test_Adding_Sibling_Is_Idempotent(ExampleTag:schemas.Tag):
    database.clear()
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.addParent(tagName, "parent")
    database.Tag.addParent(tagName, "parent")
    assert database.Tag.get("test").parents == ["parent"]


def test_Removing_Sibling_Is_Idempotent(ExampleTag:schemas.Tag):
    database.clear()
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.removeSibling(tagName, "parent")
    assert database.Tag.get("test").parents == []

