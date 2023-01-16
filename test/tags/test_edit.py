from modules import tags, database, schemas
import pytest


@pytest.fixture
def ExampleTag() -> schemas.Tag:
    database.Tag.clear()
    tag = schemas.Tag(name="test")
    database.Tag.insert(tag)
    return tag



@pytest.mark.asyncio
async def test_Invalid_Tag_Raises_Error(ExampleTag: schemas.Tag):
    with pytest.raises(tags.TagEditFailure):
        await tags.edit("Invalid",namespace="meta")



@pytest.mark.asyncio
async def test_Empty_Edit_Raises_Error(ExampleTag: schemas.Tag):
    with pytest.raises(tags.TagEditFailure):
        await tags.edit(ExampleTag.name)



@pytest.mark.asyncio
async def test_Copied_Edit_Raises_Error(ExampleTag: schemas.Tag):
    with pytest.raises(tags.TagEditFailure):
        await tags.edit(
            ExampleTag.name,
            namespace=ExampleTag.namespace,
            parents=ExampleTag.parents,
            siblings=ExampleTag.siblings,
        )



@pytest.mark.asyncio
async def test_Bad_Namespace_Raises_Error(ExampleTag: schemas.Tag):
    with pytest.raises(tags.TagEditFailure):
        await tags.edit(
            ExampleTag.name,
            namespace="INVALID",
        )



@pytest.mark.asyncio
async def test_Edit_Returns_Changes(ExampleTag: schemas.Tag):
    tag = ExampleTag
    new_tag = await tags.edit(
        tag.name,
        namespace="example",
        parents=["example_parent"],
        siblings=["example_sibling"],
        valid_namespaces=["example"]
    )
    assert new_tag.namespace == "example"
    assert new_tag.parents == ["example_parent"]
    assert new_tag.siblings == ["example_sibling"]



@pytest.mark.asyncio
async def test_Edit_Applies_Changes(ExampleTag: schemas.Tag):
    tag = ExampleTag
    await tags.edit(
        tag.name,
        namespace="example",
        parents=["example_parent"],
        siblings=["example_sibling"],
        valid_namespaces=["example"]
    )
    new_tag = database.Tag.get(tag.name)
    assert new_tag.namespace == "example"
    assert new_tag.parents == ["example_parent"]
    assert new_tag.siblings == ["example_sibling"]
