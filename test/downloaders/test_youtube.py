from modules import downloaders
import pytest

youtube = downloaders.Youtube()
SkipCondition = pytest.mark.skipif(youtube.functional == False, reason="Twitter Not Functional")


@SkipCondition
@pytest.mark.asyncio
async def test_Importing_Regular_Youtube_Video():
    await assertImport("https://www.youtube.com/watch?v=YlLn5DXTRxI")


@SkipCondition
@pytest.mark.asyncio
async def test_Importing_Short_URL_Youtube_Video():
    await assertImport("https://youtu.be/YlLn5DXTRxI")


@SkipCondition
@pytest.mark.asyncio
async def test_Importing_Youtube_Video_With_Parameters():
    await assertImport("https://www.youtube.com/watch?v=YlLn5DXTRxI&ab_channel=KawaguchiIngen")


@SkipCondition
@pytest.mark.asyncio
async def test_Valid_URL_Check():
    assert youtube.is_valid_url("https://www.youtube.com/watch?v=YlLn5DXTRxI") ,"Regular Domain"
    assert youtube.is_valid_url("https://youtube.com/watch?v=YlLn5DXTRxI") ,"Root Domain"
    assert youtube.is_valid_url("https://youtu.be/YlLn5DXTRxI") ,"Shortened Domain"
    assert youtube.is_valid_url("https://www.youtube.com/watch?v=YlLn5DXTRxI&ab_channel=KawaguchiIngen") ,"With Parameters"
    assert not youtube.is_valid_url("http://www.example.com") ,"Non HTTPS"
    assert not youtube.is_valid_url("https://www.example.com") ,"Invalid URL"
    assert not youtube.is_valid_url("https://youtu.be.example.com") ,"Invalid URL"


async def assertImport(url:str):
    posts = await youtube.download_url(url)
    
    assert len(posts) == 1
    post = posts[0]
    assert post.media_type == "video"
    assert post.full.width == 1280
    assert post.full.height == 720
    assert post.source == "https://youtube.com/watch?v=YlLn5DXTRxI"
    assert "kawaguchi_ingen" in post.tags