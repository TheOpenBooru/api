from modules.importers import SafebooruDownloader
import pytest


@pytest.fixture
def safebooru():
    return SafebooruDownloader()


async def test_Rule34_Check_URL(safebooru: SafebooruDownloader):
    assert safebooru.is_valid_url("https://safebooru.org/index.php?page=post&s=view&id=4185046")
    assert safebooru.is_valid_url("https://safebooru.org/index.php?page=post&s=view&id=4185046&test=1")
    assert not safebooru.is_valid_url("https://rule34.xxx/index.php?page=post&s=view&id=4185046")
    assert not safebooru.is_valid_url("https://safebooru.org/index.php?page=post&s=list")
    assert not safebooru.is_valid_url("https://safebooru.org/index.php?page=pool&s=show&id=21185")


@pytest.mark.asyncio
async def test_Importing_Image(safebooru: SafebooruDownloader):
    url = "https://safebooru.org/index.php?page=post&s=view&id=4185046"
    posts = await safebooru.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.type == "image"
    assert post.full.width == 2500
    assert post.full.height == 1455
    assert len(post.tags) > 10


@pytest.mark.asyncio
async def test_Importing_Animation(safebooru: SafebooruDownloader):
    url = "https://safebooru.org/index.php?page=post&s=view&id=4100857"
    posts = await safebooru.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.type == "animation"
    assert post.full.width == 600
    assert post.full.height == 600
    assert len(post.tags) > 10

