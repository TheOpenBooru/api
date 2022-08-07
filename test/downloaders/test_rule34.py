from modules import downloaders
import pytest

r34 = downloaders.Rule34()
SkipCondition = pytest.mark.skipif(r34.functional == False, reason="Twitter Not Functional")


@SkipCondition
@pytest.mark.asyncio
async def test_Rule34_Check_URL():
    assert r34.is_valid_url("https://rule34.xxx/index.php?page=post&s=view&id=5198120")
    assert r34.is_valid_url("https://rule34.xxx/index.php?page=post&s=view&id=5198120&test=1")
    assert not r34.is_valid_url("https://rule34.xxx/index.php?page=post&s=list")
    assert not r34.is_valid_url("https://rule34.xxx/index.php?page=pool&s=show&id=21185")


@SkipCondition
@pytest.mark.asyncio
async def test_Importing_Image():
    url = "https://rule34.xxx/index.php?page=post&s=view&id=5198120"
    posts = await r34.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "image"
    assert post.full.width == 1534
    assert post.full.height == 1494
    assert len(post.tags) > 10


@SkipCondition
@pytest.mark.asyncio
async def test_Importing_Animation():
    url = "https://rule34.xxx/index.php?page=post&s=view&id=4138445"
    posts = await r34.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "animation"
    assert post.full.width == 600
    assert post.full.height == 856
    assert len(post.tags) > 10


@SkipCondition
@pytest.mark.asyncio
async def test_Importing_Video():
    url = "https://rule34.xxx/index.php?page=post&s=view&id=3506721"
    posts = await r34.download_url(url)
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "video"
    assert post.full.width == 1280
    assert post.full.height == 720
    assert len(post.tags) > 10
