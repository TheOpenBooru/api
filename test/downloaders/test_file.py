from modules import downloaders
import pytest


@pytest.fixture
def file() -> downloaders.File:
    return downloaders.File()

@pytest.mark.asyncio
async def test_File_url_Importing_PNG(file):
    ...

@pytest.mark.asyncio
async def test_File_url_Importing_JPEG(file: downloaders.File):
    url = "https://i.imgur.com/XMNnx42.jpeg"
    posts = await file.download_url(url)


@pytest.mark.asyncio
async def test_File_url_Importing_WEBP():
    ...


@pytest.mark.asyncio
async def test_File_url_Importing_WEBM():
    ...


@pytest.mark.asyncio
async def test_File_url_Importing_MP4():
    ...
