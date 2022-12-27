from modules import schemas
from modules.importers import YoutubeDownloader
import pytest


@pytest.fixture
def youtube():
    return YoutubeDownloader()



@pytest.mark.asyncio
async def test_Importing_Regular_Youtube_Video(youtube: YoutubeDownloader):
    await assertImport(youtube, "https://www.youtube.com/watch?v=YlLn5DXTRxI")



@pytest.mark.asyncio
async def test_Importing_Short_URL_Youtube_Video(youtube: YoutubeDownloader):
    await assertImport(youtube, "https://youtu.be/YlLn5DXTRxI")



@pytest.mark.asyncio
async def test_Importing_Youtube_Video_With_Parameters(youtube: YoutubeDownloader):
    await assertImport(youtube, "https://www.youtube.com/watch?v=YlLn5DXTRxI&ab_channel=KawaguchiIngen")



@pytest.mark.asyncio
async def test_Valid_URL_Check(youtube: YoutubeDownloader):
    assert youtube.is_valid_url("https://www.youtube.com/watch?v=YlLn5DXTRxI") ,"Regular Domain"
    assert youtube.is_valid_url("https://youtube.com/watch?v=YlLn5DXTRxI") ,"Root Domain"
    assert youtube.is_valid_url("https://youtu.be/YlLn5DXTRxI") ,"Shortened Domain"
    assert youtube.is_valid_url("https://www.youtube.com/watch?v=YlLn5DXTRxI&ab_channel=KawaguchiIngen") ,"With Parameters"
    assert not youtube.is_valid_url("http://www.example.com") ,"Non HTTPS"
    assert not youtube.is_valid_url("https://www.example.com") ,"Invalid URL"
    assert not youtube.is_valid_url("https://youtu.be.example.com") ,"Invalid URL"


async def assertImport(youtube: YoutubeDownloader, url:str):
    posts = await youtube.download_url(url)
    
    assert len(posts) == 1
    post = posts[0]
    assert post.full.type == schemas.MediaType.video
    assert post.full.width in (1280, 640)
    assert post.full.height in (720, 358)
    assert "https://youtube.com/watch?v=YlLn5DXTRxI" in post.sources
    assert "kawaguchi_ingen" in post.tags