from modules import importers
import pytest


@pytest.fixture
def file() -> importers.FileDownloader:
    return importers.FileDownloader()


async def test_File_url_Importing_PNG(file):
    ...


async def test_File_url_Importing_JPEG(file: importers.FileDownloader):
    url = "https://i.imgur.com/XMNnx42.jpeg"
    posts = await file.download_url(url)


async def test_File_url_Importing_WEBP():
    ...


async def test_File_url_Importing_WEBM():
    ...


async def test_File_url_Importing_MP4():
    ...
