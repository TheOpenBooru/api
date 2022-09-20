from . import ClearDatabase, ExamplePost, ExampleTag
from modules import database, schemas
import pytest


def test_Add_Sibling(ClearDatabase, ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.addSibling(tagName, "sibling")
    assert database.Tag.get("test").siblings == ["sibling"]


def test_Remove_Sibling(ClearDatabase, ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.addSibling(tagName,"sibling")
    database.Tag.removeSibling(tagName,"sibling")
    assert database.Tag.get("test").siblings == []


def test_Adding_Sibling_Is_Idempotent(ClearDatabase, ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.addSibling(tagName, "sibling")
    database.Tag.addSibling(tagName, "sibling")
    assert database.Tag.get("test").siblings == [ "sibling"]


def test_Removing_Sibling_Is_Idempotent(ClearDatabase, ExampleTag:schemas.Tag):
    tagName = ExampleTag.name
    database.Tag.insert(ExampleTag)
    database.Tag.removeSibling(tagName, "sibling")
    assert database.Tag.get("test").siblings == []

