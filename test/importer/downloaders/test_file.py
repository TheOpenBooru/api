from modules import importers
import pytest


@pytest.fixture
def file() -> importers.FileDownloader:
    return importers.FileDownloader()

@pytest.mark.asyncio
async def test_File_url_Importing_PNG(file):
    ...

@pytest.mark.asyncio
async def test_File_url_Importing_JPEG(file: importers.FileDownloader):
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
