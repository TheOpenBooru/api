from . import ClearDatabase, ExamplePost, ExampleTag
from modules import database, schemas


def test_Add_Parent(ClearDatabase, ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.addParent(tagName, "parent")
    assert database.Tag.get("test").parents == ["parent"]


def test_Remove_Parent(ClearDatabase, ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.addParent(tagName,"parent")
    database.Tag.removeParent(tagName,"parent")
    assert database.Tag.get("test").parents == []


def test_Adding_Sibling_Is_Idempotent(ClearDatabase, ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.addParent(tagName, "parent")
    database.Tag.addParent(tagName, "parent")
    assert database.Tag.get("test").parents == ["parent"]


def test_Removing_Sibling_Is_Idempotent(ClearDatabase, ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.removeSibling(tagName, "parent")
    assert database.Tag.get("test").parents == []

